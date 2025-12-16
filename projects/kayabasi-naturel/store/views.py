from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import stripe

# stripe.error may not be importable in some environments; fall back so tests can run
try:
    from stripe.error import SignatureVerificationError
except Exception:
    class SignatureVerificationError(Exception):
        pass

from .models import Product, Category, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    return render(request, 'store/index.html')


def category_products(request, category_type):
    if category_type == 'ari':
        products = Product.objects.filter(category__name__icontains='arı').order_by('name')
        category_name = 'Arı Ürünleri'
        category_icon = '🐝'
    elif category_type == 'zeytin':
        products = Product.objects.filter(category__name__icontains='zeytin').order_by('name')
        category_name = 'Zeytin Ürünleri'
        category_icon = '🫒'
    else:
        products = Product.objects.none()
        category_name = 'Ürünler'
        category_icon = '📦'
    
    context = {
        'products': products,
        'category_name': category_name,
        'category_icon': category_icon,
    }
    return render(request, 'store/category.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', {'product': product})


def about(request):
    return render(request, 'about.html')


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart', {})
    qty = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    item = cart.get(slug, {'quantity': 0, 'price': str(product.price), 'name': product.name})
    item['quantity'] = item.get('quantity', 0) + qty
    cart[slug] = item
    request.session['cart'] = cart
    return redirect('store:index')


def view_cart(request):
    cart = request.session.get('cart', {})
    total = 0
    items = []
    for slug, data in cart.items():
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            continue
        quantity = data.get('quantity', 0)
        price = product.price
        items.append({'product': product, 'quantity': quantity, 'total': price * quantity})
        total += price * quantity
    return render(request, 'store/cart_v2.html', {'items': items, 'total': total})


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:index')

    if request.method == 'POST':
        # create order
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address')
        city = request.POST.get('city', '')
        district = request.POST.get('district', '')
        postal_code = request.POST.get('postal_code', '')
        order_notes = request.POST.get('order_notes', '')
        
        order = Order.objects.create(
            full_name=full_name, 
            email=email, 
            phone=phone,
            address=address,
            city=city,
            district=district,
            postal_code=postal_code,
            order_notes=order_notes
        )
        
        total_amount = 0
        for slug, data in cart.items():
            try:
                product = Product.objects.get(slug=slug)
            except Product.DoesNotExist:
                continue
            qty = data.get('quantity', 1)
            OrderItem.objects.create(order=order, product=product, price=product.price, quantity=qty)
            total_amount += float(product.price) * qty

        # create Stripe PaymentIntent (only if API keys are configured)
        if settings.STRIPE_SECRET_KEY:
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(total_amount * 100),
                    currency='try',
                    metadata={'order_id': order.id}
                )
                order.stripe_payment_intent = intent.get('id')
                order.save()
            except Exception as e:
                # Stripe hatası olsa bile siparişi kaydet
                pass
        
        # store order id in session for success page
        request.session['last_order_id'] = order.id
        # clear cart
        request.session['cart'] = {}
        # redirect to success page
        return redirect('store:order_success')

    # GET -> show checkout form
    cart = request.session.get('cart', {})
    items = []
    total = 0
    kargo = 0  # Kargo ücreti - gerekirse eklenebilir
    
    for slug, data in cart.items():
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            continue
        qty = data.get('quantity', 0)
        subtotal = product.price * qty
        items.append({
            'product': product, 
            'quantity': qty, 
            'subtotal': subtotal
        })
        total += subtotal
    
    genel_toplam = total + kargo
    
    context = {
        'items': items,
        'total': total,
        'kargo': kargo,
        'genel_toplam': genel_toplam,
        'stripe_pub': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'store/checkout.html', context)


def order_success(request):
    order_id = request.session.get('last_order_id')
    order = None
    if order_id:
        order = Order.objects.filter(id=order_id).first()
    # clear cart
    request.session['cart'] = {}
    return render(request, 'store/order_success.html', {'order': order})


def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    if not webhook_secret:
        return HttpResponse('Webhook secret not configured', status=500)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        return HttpResponse(status=400)
    except SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order_id = intent.get('metadata', {}).get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.paid = True
                order.save()
            except Order.DoesNotExist:
                pass

    return JsonResponse({'status': 'received'})
