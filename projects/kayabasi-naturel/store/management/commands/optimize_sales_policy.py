"""
Satış politikasını optimize et: Minimum, step ve unit ayarlarını en iyi uygulamalara göre ayarla.
"""
from django.core.management.base import BaseCommand
from store.models import Product


class Command(BaseCommand):
    help = 'Ürünlerin satış politikasını optimize et (minimum, step, unit)'

    def handle(self, *args, **options):
        # Ürün isimleri ile optimal politikalar
        policies = {
            # Polen: gram cinsinden, minimum 50g, step 50g
            'polen': {
                'available_units': ['g'],
                'min_order_amounts': {'g': 50},
                'quantity_steps': {'g': 50},
                'note': 'Polen: 50g adımlar, minimum 50g'
            },
            # Propolis: gram cinsinden, minimum 50g, step 25g
            'propolis': {
                'available_units': ['g'],
                'min_order_amounts': {'g': 50},
                'quantity_steps': {'g': 25},
                'note': 'Propolis: 25g adımlar, minimum 50g'
            },
            # Bal: gram/kg, minimum 250g, step 250g
            'bal': {
                'available_units': ['g', 'kg'],
                'min_order_amounts': {'g': 250, 'kg': 1},
                'quantity_steps': {'g': 250, 'kg': 1},
                'note': 'Bal: 250g adımlar, minimum 250g'
            },
            # Petek: gram/kg, minimum 100g, step 100g
            'petek': {
                'available_units': ['g', 'kg'],
                'min_order_amounts': {'g': 100, 'kg': 1},
                'quantity_steps': {'g': 100, 'kg': 1},
                'note': 'Petek: 100g adımlar, minimum 100g'
            },
            # Zeytinyağı: ml/l, minimum 250ml, step 250ml
            'zeytinyağı': {
                'available_units': ['ml', 'l'],
                'min_order_amounts': {'ml': 250, 'l': 1},
                'quantity_steps': {'ml': 250, 'l': 1},
                'note': 'Zeytinyağı: 250ml adımlar, minimum 250ml'
            },
            # Zeytin: gram/kg, minimum 250g, step 250g
            'zeytin': {
                'available_units': ['g', 'kg'],
                'min_order_amounts': {'g': 250, 'kg': 1},
                'quantity_steps': {'g': 250, 'kg': 1},
                'note': 'Zeytin: 250g adımlar, minimum 250g'
            },
        }

        # Tüm ürünler üzerinde döngü
        for product in Product.objects.all():
            product_name_lower = product.name.lower()
            
            # Her politika için kontrol et
            for keyword, policy in policies.items():
                if keyword in product_name_lower:
                    # Politikayı uygula
                    product.available_units = policy['available_units']
                    product.min_order_amounts = policy['min_order_amounts']
                    product.quantity_steps = policy['quantity_steps']
                    product.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ {product.name}: {policy['note']}"
                        )
                    )
                    break
            else:
                # Eşleşme yoksa varsayılan ayarlar
                if not product.available_units:
                    product.available_units = ['g']
                    product.min_order_amounts = {'g': 50}
                    product.quantity_steps = {'g': 50}
                    product.save()
                    self.stdout.write(
                        self.style.WARNING(
                            f"⚠ {product.name}: Varsayılan 50g ayarları uygulandı"
                        )
                    )

        self.stdout.write(self.style.SUCCESS('Satış politikası optimizasyonu tamamlandı!'))
