from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Order, OrderItem, ProductImage, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)





class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'get_total')
    can_delete = False
    
    def get_total(self, obj):
        return f"{obj.price * obj.quantity} TL"
    get_total.short_description = 'Toplam'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'city', 'order_total', 'status_badge', 'paid', 'created_at')
    list_filter = ('status', 'paid', 'created_at', 'city')
    search_fields = ('full_name', 'email', 'phone', 'address', 'city', 'district')
    readonly_fields = ('created_at', 'updated_at', 'stripe_payment_intent', 'order_total')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Sipariş Bilgileri', {
            'fields': ('created_at', 'updated_at', 'status', 'order_total', 'paid', 'stripe_payment_intent')
        }),
        ('Müşteri Bilgileri', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Teslimat Bilgileri', {
            'fields': ('address', 'city', 'district', 'postal_code')
        }),
        ('Ek Bilgiler', {
            'fields': ('order_notes',),
            'classes': ('collapse',)
        }),
    )
    
    def order_number(self, obj):
        return f"#{obj.id}"
    order_number.short_description = 'Sipariş No'
    
    def order_total(self, obj):
        total = obj.get_total()
        return f"{total} TL"
    order_total.short_description = 'Toplam Tutar'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#17a2b8',
            'processing': '#007bff',
            'shipped': '#6f42c1',
            'delivered': '#28a745',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        text = dict(obj.STATUS_CHOICES).get(obj.status, obj.status)
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, text
        )
    status_badge.short_description = 'Durum'
    
    def payment_status(self, obj):
        if obj.paid:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Ödendi</span>')
        return format_html('<span style="background-color: #ffc107; color: black; padding: 3px 10px; border-radius: 3px;">Bekliyor</span>')
    payment_status.short_description = 'Ödeme'
    
    actions = [
        'mark_as_pending',
        'mark_as_confirmed',
        'mark_as_processing',
        'mark_as_shipped',
        'mark_as_delivered',
        'mark_as_cancelled',
        'mark_as_paid',
        'mark_as_unpaid',
    ]
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} sipariş "Beklemede" olarak güncellendi.')
    mark_as_pending.short_description = '✓ Durum: Beklemede'
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} sipariş "Onaylandı" olarak güncellendi.')
    mark_as_confirmed.short_description = '✓ Durum: Onaylandı'
    
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} sipariş "Hazırlanıyor" olarak güncellendi.')
    mark_as_processing.short_description = '✓ Durum: Hazırlanıyor'
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} sipariş "Gönderildi" olarak güncellendi.')
    mark_as_shipped.short_description = '✓ Durum: Gönderildi'
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} sipariş "Teslim Edildi" olarak güncellendi.')
    mark_as_delivered.short_description = '✓ Durum: Teslim Edildi'
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} sipariş "İptal Edildi" olarak güncellendi.')
    mark_as_cancelled.short_description = '✗ Durum: İptal Edildi'
    
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(paid=True)
        self.message_user(request, f'{updated} sipariş ödendi olarak işaretlendi.')
    mark_as_paid.short_description = 'Ödendi olarak işaretle'
    
    def mark_as_unpaid(self, request, queryset):
        updated = queryset.update(paid=False)
        self.message_user(request, f'{updated} sipariş ödeme bekliyor olarak işaretlendi.')
    mark_as_unpaid.short_description = 'Ödeme bekliyor olarak işaretle'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_main', 'order')
    ordering = ('order', 'created_at')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'is_main', 'order')
    list_filter = ('product', 'is_main')
    list_editable = ('is_main', 'order')
    ordering = ('product', 'order')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.image.url
            )
        return "Resim Yok"
    image_preview.short_description = 'Ön İzleme'


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'created_at', 'updated_at')
    can_delete = True
    fields = ('user', 'rating', 'title', 'is_approved', 'created_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating_stars', 'title', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'product', 'created_at')
    search_fields = ('product__name', 'user__username', 'title', 'comment')
    readonly_fields = ('user', 'created_at', 'updated_at', 'helpful_count')
    list_editable = ('is_approved',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Yorum Bilgileri', {
            'fields': ('product', 'user', 'rating', 'title', 'comment')
        }),
        ('Durum', {
            'fields': ('is_approved', 'helpful_count')
        }),
        ('Tarihler', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html(
            '<span style="color: #ffc107; font-weight: bold;">{} ({})</span>',
            stars, obj.rating
        )
    rating_stars.short_description = 'Puan'


# ProductAdmin güncellendi - aşağıda tanımlı
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'stock_status', 'avg_rating', 'review_count', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description', 'production_location')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock')
    readonly_fields = ('created_at', 'slug', 'avg_rating', 'review_count')
    inlines = [ProductImageInline, ReviewInline]
    
    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('Fiyat ve Stok', {
            'fields': ('price', 'stock', 'unit')
        }),
        ('Üretim Bilgileri', {
            'fields': ('production_location', 'production_process', 'production_date', 'harvest_date'),
            'classes': ('collapse',)
        }),
        ('Ürün Detayları', {
            'fields': ('weight', 'shelf_life', 'ingredients', 'storage_conditions', 'certificates'),
            'classes': ('collapse',)
        }),
        ('İstatistikler', {
            'fields': ('avg_rating', 'review_count'),
            'classes': ('collapse',)
        }),
        ('Tarihler', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color: red; font-weight: bold;">Tükendi</span>')
        elif obj.stock < 10:
            return format_html('<span style="color: orange; font-weight: bold;">Az Kaldı ({})</span>', obj.stock)
        else:
            return format_html('<span style="color: green;">Stokta ({})</span>', obj.stock)
    stock_status.short_description = 'Stok Durumu'
    
    def avg_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if not reviews.exists():
            return "Yorum Yok"
        avg = sum(r.rating for r in reviews) / reviews.count()
        stars = '⭐' * int(avg)
        return format_html(
            '<span style="color: #ffc107; font-weight: bold;">{} ({:.1f})</span>',
            stars, avg
        )
    avg_rating.short_description = 'Ort. Puan'
    
    def review_count(self, obj):
        count = obj.reviews.filter(is_approved=True).count()
        return format_html(
            '<span style="background-color: #e9ecef; padding: 3px 8px; border-radius: 3px;">{} Yorum</span>',
            count
        )
    review_count.short_description = 'Yorum Sayı'

