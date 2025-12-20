"""
Paket fiyatlarını gram oranına göre otomatik hesapla.
En küçük paket (50g) base fiyat olarak kullanılır.
"""
from django.core.management.base import BaseCommand
from store.models import Product
import re


def extract_grams(size_str):
    """'50g' -> 50, '1kg' -> 1000, '250ml' -> 250"""
    match = re.search(r'(\d+)\s*(g|kg|ml|l)', size_str.lower())
    if not match:
        return None
    
    value = int(match.group(1))
    unit = match.group(2)
    
    if unit == 'kg':
        return value * 1000
    elif unit == 'l':
        return value * 1000
    return value


class Command(BaseCommand):
    help = 'Paket fiyatlarını gram/ml oranına göre otomatik hesapla'

    def handle(self, *args, **options):
        updated = 0
        
        for product in Product.objects.all():
            if not product.packages:
                continue
            
            # Paketleri grama göre sırala
            packages_with_grams = []
            for pkg in product.packages:
                grams = extract_grams(pkg['size'])
                if grams:
                    packages_with_grams.append((grams, pkg))
            
            if not packages_with_grams:
                continue
            
            # En küçük paket base olur (bu fiyat product.price olmalı)
            packages_with_grams.sort()
            min_grams, min_pkg = packages_with_grams[0]
            base_price = float(product.price)
            price_per_gram = base_price / min_grams
            
            # Tüm paketlerin fiyatını hesapla
            for i, pkg in enumerate(product.packages):
                grams = extract_grams(pkg['size'])
                if grams:
                    calculated_price = float(round(grams * price_per_gram, 2))
                    product.packages[i]['price'] = calculated_price
            
            product.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ {product.name}: Fiyatlar gram oranına göre hesaplandı ({price_per_gram:.2f}₺/g)"
                )
            )
            updated += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n{updated} ürün güncellenmiştir!'))
