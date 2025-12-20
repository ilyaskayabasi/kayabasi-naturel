from django.core.management.base import BaseCommand
from store.models import Product

DEFAULT_STEPS = {
    'g': 50,
    'kg': 1,
    'ml': 100,
    'l': 1,
    'adet': 1,
}

class Command(BaseCommand):
    help = "Set default quantity steps per unit for products (does not overwrite explicit values)"

    def handle(self, *args, **options):
        updated = 0
        for product in Product.objects.all():
            steps = product.quantity_steps or {}
            changed = False
            for unit in (product.available_units or [product.unit]):
                if unit not in steps:
                    default = DEFAULT_STEPS.get(unit, 1)
                    steps[unit] = default
                    changed = True
            if changed:
                product.quantity_steps = steps
                product.save()
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Quantity steps set/filled for {updated} products."))
