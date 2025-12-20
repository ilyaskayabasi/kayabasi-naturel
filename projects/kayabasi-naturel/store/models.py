from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram (kg)'),
        ('g', 'Gram (g)'),
        ('ml', 'Mililitre (ml)'),
        ('l', 'Litre (l)'),
        ('adet', 'Adet'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='adet', verbose_name="Ölçü Birimi")
    available_units = models.JSONField(default=list, verbose_name="Mevcut Ölçü Birimleri", help_text="Müşterilerin seçebileceği ölçü birimleri (kg, g, ml, l, adet)")
    min_order_amounts = models.JSONField(default=dict, verbose_name="Minimum Sipariş Miktarları", help_text="Ölçü birimine göre minimum miktar (ör. {'g': 50, 'kg': 1})")
    quantity_steps = models.JSONField(default=dict, verbose_name="Sipariş Artış Adımı", help_text="Ölçü birimine göre sipariş artış adımı (ör. {'g': 50, 'kg': 1, 'l': 1})")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Detaylı ürün bilgileri
    production_date = models.DateField(null=True, blank=True, verbose_name="Üretim Tarihi")
    production_location = models.CharField(max_length=200, default="Milas, Muğla", verbose_name="Üretim Yeri")
    harvest_date = models.DateField(null=True, blank=True, verbose_name="Hasat Tarihi")
    production_process = models.TextField(blank=True, verbose_name="Üretim Süreci")
    ingredients = models.TextField(blank=True, verbose_name="İçerik Bilgisi")
    storage_conditions = models.TextField(blank=True, verbose_name="Saklama Koşulları")
    shelf_life = models.CharField(max_length=100, blank=True, verbose_name="Raf Ömrü")
    weight = models.CharField(max_length=50, blank=True, verbose_name="Net Ağırlık")
    certificates = models.TextField(blank=True, verbose_name="Sertifikalar")

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('confirmed', 'Onaylandı'),
        ('processing', 'Hazırlanıyor'),
        ('shipped', 'Gönderildi'),
        ('delivered', 'Teslim Edildi'),
        ('cancelled', 'İptal Edildi'),
    ]
    
    full_name = models.CharField(max_length=200, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, verbose_name="Telefon", default="")
    address = models.TextField(verbose_name="Adres")
    city = models.CharField(max_length=100, verbose_name="İl", default="")
    district = models.CharField(max_length=100, verbose_name="İlçe", default="")
    postal_code = models.CharField(max_length=10, verbose_name="Posta Kodu", blank=True, default="")
    order_notes = models.TextField(verbose_name="Sipariş Notu", blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Durum")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")
    paid = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"

    def __str__(self):
        return f"Sipariş #{self.id} - {self.full_name}"
    
    def get_total(self):
        return sum(item.price * item.quantity for item in self.items.all())
    
    def get_status_display_tr(self):
        return dict(self.STATUS_CHOICES).get(self.status)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="Ürün")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Resim")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Alt Metin")
    is_main = models.BooleanField(default=False, verbose_name="Ana Resim")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Ürün Resmi"
        verbose_name_plural = "Ürün Resimleri"

    def __str__(self):
        return f"{self.product.name} - Resim {self.order}"


class Review(models.Model):
    RATING_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ 5 Yıldız'),
        (4, '⭐⭐⭐⭐ 4 Yıldız'),
        (3, '⭐⭐⭐ 3 Yıldız'),
        (2, '⭐⭐ 2 Yıldız'),
        (1, '⭐ 1 Yıldız'),
    ]

    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name="Ürün")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Puan")
    title = models.CharField(max_length=200, verbose_name="Başlık")
    comment = models.TextField(verbose_name="Yorum")
    is_approved = models.BooleanField(default=True, verbose_name="Onaylı")
    helpful_count = models.PositiveIntegerField(default=0, verbose_name="Faydalı Say")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}⭐)"

    def get_rating_display_star(self):
        return '⭐' * self.rating

