# Kayabaşı Naturel - Django E-Ticaret Platformu

Modern ve performanslı bir e-ticaret sitesi. Doğal arı ürünleri ve zeytincilik ürünlerinin satışı için tasarlanmıştır.

## 🚀 Özellikler

- ✅ **Kategori Sayfaları**: Banner, breadcrumb, sıralama, hover animasyonları
- ✅ **Ürün Detay**: Galeri, paket seçimi, dinamik fiyatlandırma, yorumlar
- ✅ **Sepet & Ödeme**: Stripe entegrasyonu, sipariş takibi
- ✅ **Responsive Tasarım**: Mobil uyumlu, optimize edilmiş
- ✅ **SEO**: Meta tags, Schema.org, sitemap
- ✅ **Admin Panel**: Sipariş yönetimi, stok takibi, yorum onaylama

## 📦 Kurulum

### Yerel Geliştirme (Windows PowerShell)

```powershell
# Proje dizinine git
cd projects\kayabasi-naturel

# Sanal ortam oluştur
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Bağımlılıkları yükle
pip install -r requirements.txt

# Veritabanı migrasyonları
python manage.py migrate

# Süper kullanıcı oluştur
python manage.py createsuperuser

# Sunucuyu başlat
python manage.py runserver
```

Site: `http://localhost:8000/`  
Admin: `http://localhost:8000/admin/`

## 🔧 Yapılandırma

### Geliştirme Ortamı

`.env` dosyası oluştur (isteğe bağlı):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe (ödeme)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Email (isteğe bağlı)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Production Deployment

```bash
# Production settings kullan
export DJANGO_SETTINGS_MODULE=config.settings_prod

# Gerekli environment variables
export SECRET_KEY='...'
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
export DATABASE_URL='postgres://user:pass@host:5432/dbname'

# Static dosyaları topla
python manage.py collectstatic --noinput

# Gunicorn ile çalıştır
gunicorn config.wsgi:application
```

## 📁 Proje Yapısı

```
kayabasi-naturel/
├── config/              # Django ayarları
│   ├── settings.py      # Geliştirme ayarları
│   ├── settings_prod.py # Production ayarları
│   └── urls.py
├── store/               # Ana uygulama
│   ├── models.py        # Ürün, Sipariş, Yorum modelleri
│   ├── views.py         # View fonksiyonları
│   ├── admin.py         # Admin panel özelleştirmeleri
│   └── management/      # Yönetim komutları
├── templates/           # HTML şablonları
├── static/              # CSS, JS, görseller
├── media/               # Kullanıcı yüklemeleri
└── requirements.txt     # Python bağımlılıkları
```

## 🎨 Özelleştirme

### Yeni Kategori Ekleme

1. `store/views.py` → `category_products` fonksiyonuna ekle
2. `templates/store/category.html` → Banner görseli ekle
3. Admin'den ürünleri kategoriye ata

### Ödeme Ayarları

Stripe dashboard'dan API anahtarlarını al ve ayarla:

```python
# settings.py
STRIPE_SECRET_KEY = 'sk_live_...'
STRIPE_PUBLISHABLE_KEY = 'pk_live_...'
```

## 📊 Yönetim Komutları

```bash
# Paket ayarlarını güncelle
python manage.py setup_packages

# Minimum sipariş miktarlarını ayarla
python manage.py set_minimums

# Veritabanını yedekle
python manage.py dumpdata > backup.json
```

## 🔒 Güvenlik

Production için:
- `DEBUG = False` ayarla
- `SECRET_KEY` değiştir
- HTTPS kullan
- `settings_prod.py` kullan
- Firewall kuralları ayarla

## 📝 Lisans

Bu proje özel kullanım içindir.

## 👥 İletişim

İlyas Kayabaşı - Kayabaşı Naturel
 - Gerçek ödeme akışı için Stripe Webhook doğrulaması ekleyin ve `Order.paid` alanını webhook ile güncelleyin.
 - Ortam değişkenleri ayarlayın: `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY` ve `STRIPE_WEBHOOK_SECRET`.
 - Para birimi: proje TL (TRY) ile çalışacak şekilde ayarlandı.
 - Webhook endpoint: `/stripe/webhook/` (bu endpoint Stripe dashboard'da tanımlanmalıdır).
 
 Sepet ve sipariş akışı özet:
 - Sepet: Session tabanlı (kullanıcı girişine bağlı değil). `add_to_cart`, `view_cart` ve `checkout` view'leri eklendi.
 - Sipariş: `Order` ve `OrderItem` modelleri oluşturuldu, admin üzerinden görüntülenebilir.
 
Docker & deploy (hızlı notlar):
- Bu klasörde bir `Dockerfile` ve `docker-compose.yml` bulunmaktadır. Basit bir Postgres servisi ile birlikte uygulamayı docker-compose ile çalıştırabilirsiniz.
- Örnek kullanım (projede `.env.example` dosyasını kopyalayıp `.env` yapın ve değerleri doldurun):

```powershell
Set-Location .\projects\kayabasi-naturel
copy .env.example .env
# Edit .env ve gerekli anahtarları ayarla
docker compose up --build
```

Stripe webhook testi (local + ngrok):
- Stripe Dashboard içinde bir webhook endpoint ekleyin; URL olarak `https://<your-ngrok>.ngrok.io/stripe/webhook/` kullanın ve event türü olarak `payment_intent.succeeded` seçin.
- Localde sunucuyu çalıştırmak için ngrok kullanın:

```powershell
ngrok http 8000
```

- Ardından Stripe Dashboard'dan test ödemesi yapın; webhook geldiğinde `Order.paid` alanı güncellenecektir.

Not: production için `DEBUG=False`, güvenli `SECRET_KEY`, HTTPS, webhook secret ve güçlü veritabanı ayarları ayarlayın.

Hızlı kurulum scriptleri:
- `.`\generate_env.py` — `.env.example`'den `.env` oluşturur ve `SECRET_KEY` üretir.
- `.`\setup_local.ps1` — PowerShell script; venv oluşturur, bağımlılıkları yükler, migrate çalıştırır ve dev sunucusunu başlatır. Süper kullanıcı yaratmak için önce ortam değişkeni `DJANGO_SUPERUSER_USERNAME` ve `DJANGO_SUPERUSER_PASSWORD` ayarlayın ve script'i `-CreateSuperUser` ile çalıştırın.

Örnek (PowerShell):
```powershell
Set-Location .\projects\kayabasi-naturel
python generate_env.py
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# veya otomatik kurulum
.\setup_local.ps1 -CreateSuperUser
```
