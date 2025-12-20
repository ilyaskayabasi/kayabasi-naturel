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
        self.prod = Product.objects.create(name='Yeşil Zeytin', price=12.0, stock=5, category=self.cat)

    def test_index_status(self):
        resp = self.client.get(reverse('store:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Ürünler')

    def test_add_to_cart_and_cart_view(self):
        add_url = reverse('store:add_to_cart', args=[self.prod.slug])
        resp = self.client.post(add_url, {'quantity': 2}, follow=True)
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
        # Context should include selectable_units with mapped labels
        selectable_units = resp.context.get('selectable_units')
        self.assertIsNotNone(selectable_units)
        self.assertIn(('g', 'Gram (g)'), selectable_units)
        self.assertIn(('kg', 'Kilogram (kg)'), selectable_units)

    def test_add_to_cart_enforces_allowed_unit(self):
        # Allowed units: g, kg; default unit g
        self.prod.unit = 'g'
        self.prod.available_units = ['g', 'kg']
        self.prod.save()

        add_url = reverse('store:add_to_cart', args=[self.prod.slug])
        # Post with allowed unit 'kg'
        resp = self.client.post(add_url, {'quantity': 1, 'unit': 'kg'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        cart = self.client.session.get('cart', {})
        self.assertIn(self.prod.slug, cart)
        self.assertEqual(cart[self.prod.slug]['unit'], 'kg')

        # Post with disallowed unit 'ml' should fallback to product.unit ('g')
        resp = self.client.post(add_url, {'quantity': 1, 'unit': 'ml'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart[self.prod.slug]['unit'], 'g')

    def test_min_order_amount_enforced(self):
        # Set minimums: g -> 50
        self.prod.unit = 'g'
        self.prod.available_units = ['g']
        self.prod.min_order_amounts = {'g': 50}
        self.prod.save()

        add_url = reverse('store:add_to_cart', args=[self.prod.slug])
        # Try below minimum
        resp = self.client.post(add_url, {'quantity': 10, 'unit': 'g'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        # Should redirect back to product_detail and not add to cart
        self.assertTemplateUsed(resp, 'store/detail.html')
        cart = self.client.session.get('cart', {})
        self.assertNotIn(self.prod.slug, cart)

        # Try at minimum
        resp = self.client.post(add_url, {'quantity': 50, 'unit': 'g'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        cart = self.client.session.get('cart', {})
        self.assertIn(self.prod.slug, cart)
        self.assertEqual(cart[self.prod.slug]['quantity'], 50)
