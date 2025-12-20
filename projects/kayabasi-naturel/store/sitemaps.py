from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return reverse('store:product_detail', args=[obj.slug])

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        # Map category names to existing category_types
        name = (obj.name or '').lower()
        if 'zeytin' in name:
            return reverse('store:category_products', args=['zeytin'])
        if 'arı' in name or 'ari' in name:
            return reverse('store:category_products', args=['ari'])
        return reverse('store:index')

class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['store:index', 'store:about', 'store:view_cart', 'store:checkout', 'store:search_products']

    def location(self, item):
        return reverse(item)
