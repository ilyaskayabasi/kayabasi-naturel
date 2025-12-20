from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product, Category


class ProductModelTest(TestCase):
    def test_create_product(self):
        cat = Category.objects.create(name='Zeytin')
        p = Product.objects.create(name='Siyah Zeytin', price=25.50, stock=10, category=cat)
        self.assertEqual(str(p), 'Siyah Zeytin')
        self.assertEqual(p.slug, 'siyah-zeytin')


class StoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='Zeytin')
        self.prod = Product.objects.create(
            name='Yeşil Zeytin',
            price=12.0,
            stock=5,
            category=self.cat,
            packages=[{'size': '250g', 'price': None}, {'size': '500g', 'price': None}]
        )

    def test_index_status(self):
        resp = self.client.get(reverse('store:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Ürünler')

    def test_add_to_cart_and_cart_view(self):
        add_url = reverse('store:add_to_cart', args=[self.prod.slug])
        resp = self.client.post(add_url, {'quantity': 2, 'package': '250g'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        cart_resp = self.client.get(reverse('store:view_cart'))
        self.assertContains(cart_resp, 'Yeşil Zeytin')

    def test_product_detail_selectable_units(self):
        # Product with specific available units
        self.prod.unit = 'g'
        self.prod.available_units = ['g', 'kg']
        self.prod.save()

        resp = self.client.get(reverse('store:product_detail', args=[self.prod.slug]))
        self.assertEqual(resp.status_code, 200)
        # Context should include packages
        packages = resp.context.get('product').packages
        self.assertIsNotNone(packages)
        self.assertEqual(len(packages), 2)

    def test_add_to_cart_enforces_allowed_unit(self):
        # Paket tabanlı sistem test
        self.prod.unit = 'g'
        self.prod.available_units = ['g', 'kg']
        self.prod.save()

        add_url = reverse('store:add_to_cart', args=[self.prod.slug])
        # Post with package
        resp = self.client.post(add_url, {'quantity': 1, 'package': '250g'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        cart = self.client.session.get('cart', {})
        self.assertIn(self.prod.slug, cart)
        self.assertEqual(cart[self.prod.slug]['package'], '250g')

    def test_min_order_amount_enforced(self):
        # Paket tabanlı sistem - minimum qty validation
        self.prod.unit = 'g'
        self.prod.available_units = ['g']
        self.prod.min_order_amounts = {'g': 50}
        self.prod.packages = [{'size': '50g', 'price': None}]
        self.prod.save()

        add_url = reverse('store:add_to_cart', args=[self.prod.slug])
        # Qty 1 should be OK (paket sisteminde adet kontrolü)
        resp = self.client.post(add_url, {'quantity': 1, 'package': '50g'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        cart = self.client.session.get('cart', {})
        self.assertIn(self.prod.slug, cart)
        self.assertEqual(cart[self.prod.slug]['quantity'], 1)

    def test_quantity_step_enforced(self):
        # Paket tabanlı sistemde step kontrolü geçerli değil
        # Paket seçimi ve adet girişi ayrı
        self.prod.unit = 'g'
        self.prod.available_units = ['g']
        self.prod.quantity_steps = {'g': 50}
        self.prod.packages = [{'size': '100g', 'price': None}]
        self.prod.save()

        add_url = reverse('store:add_to_cart', args=[self.prod.slug])
        # Herhangi bir adet OK (paket zaten seçilmiş)
        resp = self.client.post(add_url, {'quantity': 3, 'package': '100g'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        cart = self.client.session.get('cart', {})
        self.assertIn(self.prod.slug, cart)
        self.assertEqual(cart[self.prod.slug]['quantity'], 3)

