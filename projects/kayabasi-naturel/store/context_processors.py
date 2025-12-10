from .models import Product


def cart_item_count(request):
    """Return cart item count for navbar display."""
    cart = request.session.get('cart', {})
    count = 0
    for data in cart.values():
        try:
            count += int(data.get('quantity', 0))
        except Exception:
            continue
    return {'cart_count': count}
