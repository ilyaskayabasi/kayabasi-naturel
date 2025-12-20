from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = "Override minimum order amounts for specific products by name keywords"

    PRODUCT_MINIMUMS = {
        'propolis': {'g': 50},
        'polen': {'g': 250, 'kg': 1},
        'zeytinya': {'l': 1},  # matches zeytinyağı
    }

    def handle(self, *args, **options):
        updated = 0
        for product in Product.objects.all():
            name = (product.name or '').lower()
            for key, mins in self.PRODUCT_MINIMUMS.items():
                if key in name:
                    product.min_order_amounts = mins
                    # Ensure unit aligns sensibly
                    if 'g' in mins and product.unit not in ['g', 'kg', 'adet', 'ml', 'l']:
                        product.unit = 'g'
                    if 'l' in mins:
                        product.unit = 'l'
                    product.save()
                    updated += 1
                    break
        self.stdout.write(self.style.SUCCESS(f"Overrode minimums for {updated} products."))
