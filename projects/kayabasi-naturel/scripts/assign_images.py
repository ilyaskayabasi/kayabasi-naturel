import os
import sys
import django
import urllib.request

# ensure project root is on sys.path so Django can import config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Product
from django.conf import settings

MEDIA_DIR = os.path.join(settings.BASE_DIR, 'media', 'products')
os.makedirs(MEDIA_DIR, exist_ok=True)

products = Product.objects.all()
if not products.exists():
    print('No products found; nothing to do.')
    exit(0)

for p in products:
    slug = p.slug or p.name.replace(' ', '-').lower()
    filename = f"{slug}.jpg"
    filepath = os.path.join(MEDIA_DIR, filename)
    if not os.path.exists(filepath):
        url = f"https://placehold.co/800x520?text={urllib.request.quote(p.name)}"
        print('Downloading', url, '->', filepath)
        try:
            urllib.request.urlretrieve(url, filepath)
        except Exception as e:
            print('Failed to download for', p.name, e)
            continue
    # assign to ImageField (store relative path inside MEDIA_ROOT)
    rel_path = os.path.join('products', filename).replace('\\','/')
    p.image.name = rel_path
    p.save()
    print('Assigned image for', p.name, '->', rel_path)

print('Done assigning images for', products.count(), 'products')
