"""
Paket tabanlı satış sistemini ürünlere uygula.
"""
from django.core.management.base import BaseCommand
from store.models import Product


class Command(BaseCommand):
    help = 'Ürünleri paket tabanlı satış sistemine dönüştür'

    def handle(self, *args, **options):
        # Paket tanımları: kategori/ürün türüne göre
        package_templates = {
            'polen': [
                {'size': '50g', 'price': None},  # None = base price kullan
                {'size': '100g', 'price': None},
                {'size': '250g', 'price': None},
                {'size': '500g', 'price': None},
                {'size': '1kg', 'price': None},
            ],
            'propolis': [
                {'size': '50g', 'price': None},
                {'size': '100g', 'price': None},
                {'size': '250g', 'price': None},
                {'size': '500g', 'price': None},
            ],
            'bal': [
                {'size': '250g', 'price': None},
                {'size': '500g', 'price': None},
                {'size': '1kg', 'price': None},
                {'size': '2kg', 'price': None},
            ],
            'petek': [
                {'size': '100g', 'price': None},
                {'size': '250g', 'price': None},
                {'size': '500g', 'price': None},
                {'size': '1kg', 'price': None},
            ],
            'zeytin': [
                {'size': '250g', 'price': None},
                {'size': '500g', 'price': None},
                {'size': '1kg', 'price': None},
                {'size': '2kg', 'price': None},
            ],
            'zeytinyağı': [
                {'size': '250ml', 'price': None},
                {'size': '500ml', 'price': None},
                {'size': '1l', 'price': None},
                {'size': '2l', 'price': None},
            ],
        }

        updated = 0
        for product in Product.objects.all():
            product_name_lower = product.name.lower()
            
            # Paket template'ini bul
            packages = None
            for keyword, template in package_templates.items():
                if keyword in product_name_lower:
                    packages = template
                    break
            
            if packages:
                product.packages = packages
                product.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ {product.name}: {len(packages)} paket eklendi"
                    )
                )
                updated += 1
            else:
                # Varsayılan paketi ekle
                product.packages = [{'size': 'Standart', 'price': None}]
                product.save()
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠ {product.name}: Varsayılan paket eklendi"
                    )
                )
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'\n{updated} ürün paket sistemine dönüştürüldü!'))
