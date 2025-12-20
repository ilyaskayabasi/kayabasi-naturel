from django.core.management.base import BaseCommand
from store.models import Product
import re

class Command(BaseCommand):
    help = "Extract minimum order amounts from product descriptions/weight and update min_order_amounts"

    def handle(self, *args, **options):
        updated = 0
        for product in Product.objects.all():
            mins = {}
            source = None

            # Try to extract from weight field (e.g., "En az 50 g")
            if product.weight:
                weight_lower = product.weight.lower()
                # Match "en az X g/kg/l/ml"
                match = re.search(r'en\s+az\s+(\d+(?:[.,]\d+)?)\s*(g|kg|ml|l)', weight_lower)
                if match:
                    amount = int(float(match.group(1).replace(',', '.')))
                    unit = match.group(2)
                    mins[unit] = amount
                    source = f"weight: {product.weight}"

            # Try to extract from description as fallback
            if not mins and product.description:
                desc_lower = product.description.lower()
                match = re.search(r'en\s+az\s+(\d+(?:[.,]\d+)?)\s*(g|kg|ml|l)', desc_lower)
                if match:
                    amount = int(float(match.group(1).replace(',', '.')))
                    unit = match.group(2)
                    mins[unit] = amount
                    source = f"description"

            # If found and different from current, update
            if mins and mins != product.min_order_amounts:
                product.min_order_amounts = mins
                product.save()
                updated += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ {product.name}: {mins} ({source})"
                    )
                )
            elif mins:
                self.stdout.write(f"  {product.name}: Already correct {mins}")

        self.stdout.write(self.style.SUCCESS(f"\nUpdated {updated} products."))
