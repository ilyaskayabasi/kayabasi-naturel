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
