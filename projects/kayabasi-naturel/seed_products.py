import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django

django.setup()

from store.models import Category, Product


def seed():
    cats = [
        ('Zeytin', 'zeytin'),
        ('Zeytinyağı', 'zeytinyagi'),
        ('Arı Ürünleri', 'ari-urunleri'),
    ]
    for name, slug in cats:
        Category.objects.get_or_create(name=name, slug=slug)

    data = [
        ('Siyah Zeytin', 'siyah-zeytin', 'Lezzetli siyah zeytin.', 40.0, 50, 'zeytin'),
        ('Naturel Sızma Zeytinyağı 500ml', 'zeytinyagi-500', 'Soğuk sıkım naturel sızma zeytinyağı.', 120.0, 20, 'zeytinyagi'),
        ('Çiçek Balı 1kg', 'cicek-bali', 'Doğal çiçek balı, katkısız.', 250.0, 15, 'ari-urunleri'),
        ('Kırma Zeytin', 'kirma-zeytin', 'Kırma zeytin, doğal salamura.', 45.0, 60, 'zeytin'),
        ('Yağlı Zeytin', 'yagli-zeytin', 'Yağlı zeytin, yumuşak dokulu.', 50.0, 40, 'zeytin'),
        ('Yeşil Zeytin', 'yesil-zeytin', 'Taze yeşil zeytin.', 48.0, 55, 'zeytin'),
        ('Dilme Zeytin', 'dilme-zeytin', 'Dilme zeytin, salatalık için ideal.', 47.0, 30, 'zeytin'),
        ('Çam Balı', 'cam-bali', 'Doğal çam balı.', 320.0, 10, 'ari-urunleri'),
        ('Petek Balı', 'petek-bali', 'Doğal petek balı.', 380.0, 8, 'ari-urunleri'),
        ('Karakovan Balı', 'karakovan-bali', 'Karakovan balı, nadir ve aromatik.', 420.0, 5, 'ari-urunleri'),
        ('Polen', 'polen', 'Doğal arı poleni, takviye amaçlı.', 85.0, 25, 'ari-urunleri'),
        ('Propolis', 'propolis', 'Saf propolis özü, doğal.', 130.0, 20, 'ari-urunleri'),
    ]

    for name, slug, desc, price, stock, cat_slug in data:
        cat = Category.objects.filter(slug=cat_slug).first()
        Product.objects.update_or_create(slug=slug, defaults={
            'name': name,
            'description': desc,
            'price': price,
            'stock': stock,
            'category': cat,
        })

    print('Seeding complete.')


if __name__ == '__main__':
    seed()
