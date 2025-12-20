from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = "Set per-unit minimum order amounts for known product types"

    def handle(self, *args, **options):
        updated = 0
        for product in Product.objects.all():
            name = (product.name or "").lower()
            mins = {}
            # Keep existing available_units unless empty; set sensible defaults if needed
            if not product.available_units:
                if "propolis" in name:
                    product.available_units = ["g"]
                elif "polen" in name:
                    product.available_units = ["g", "kg"]
                elif "zeytinya" in name:  # matches zeytinyağı
                    product.available_units = ["l"]
                else:
                    product.available_units = [product.unit or "kg"]

            # Set minimums based on known types
            if "propolis" in name:
                mins = {"g": 50}
                product.unit = "g"
            elif "polen" in name:
                mins = {"g": 50, "kg": 1}
                if product.unit not in ["g", "kg"]:
                    product.unit = "g"
            elif "zeytinya" in name:
                mins = {"l": 1}
                product.unit = "l"
            else:
                # Default: minimum 1 in current unit
                base_unit = product.unit or "kg"
                mins = {base_unit: 1}

            product.min_order_amounts = mins
            product.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Minimums set for {updated} products."))
