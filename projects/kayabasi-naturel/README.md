# Kayabaşı Naturel - Django Scaffold

Bu klasör yerel geliştirme için hızlı bir Django iskeleti içerir.

Hızlı başlatma (PowerShell):

```powershell
# proje dizinine gidin
Set-Location .\projects\kayabasi-naturel

# sanal ortam oluştur ve aktive et
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# bağımlılıkları yükle
pip install -r requirements.txt

# ilk migrate ve süper kullanıcı
python manage.py migrate
python manage.py createsuperuser

# sunucuyu başlat
python manage.py runserver
```

 Notlar:
 - `settings.py` içinde `SECRET_KEY` üretip değiştirin (üretim için).
 - Ödeme entegrasyonu (örnek Stripe) iskeleti bu scaffold'a eklendi. Geliştirmek için:
 
 - Ortam değişkenleri ayarlayın: `STRIPE_SECRET_KEY` ve `STRIPE_PUBLISHABLE_KEY`.
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
