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
