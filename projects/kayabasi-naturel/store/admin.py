from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'stock_status', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description', 'production_location')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock')
    readonly_fields = ('created_at', 'slug')
    
    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('Fiyat ve Stok', {
            'fields': ('price', 'stock')
        }),
        ('Üretim Bilgileri', {
            'fields': ('production_location', 'production_process', 'production_date', 'harvest_date'),
            'classes': ('collapse',)
        }),
        ('Ürün Detayları', {
            'fields': ('weight', 'shelf_life', 'ingredients', 'storage_conditions', 'certificates'),
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
    list_display = ('order_number', 'full_name', 'phone', 'city', 'order_total', 'payment_status', 'created_at')
    list_filter = ('paid', 'created_at', 'city')
    search_fields = ('full_name', 'email', 'phone', 'address', 'city', 'district')
    readonly_fields = ('created_at', 'stripe_payment_intent', 'order_total')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Sipariş Bilgileri', {
            'fields': ('created_at', 'order_total', 'paid', 'stripe_payment_intent')
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
    
    def payment_status(self, obj):
        if obj.paid:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Ödendi</span>')
        else:
            return format_html('<span style="background-color: #ffc107; color: black; padding: 3px 10px; border-radius: 3px;">Bekliyor</span>')
    payment_status.short_description = 'Ödeme Durumu'
    
    actions = ['mark_as_paid', 'mark_as_unpaid']
    
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(paid=True)
        self.message_user(request, f'{updated} sipariş ödendi olarak işaretlendi.')
    mark_as_paid.short_description = 'Seçili siparişleri ödendi olarak işaretle'
    
    def mark_as_unpaid(self, request, queryset):
        updated = queryset.update(paid=False)
        self.message_user(request, f'{updated} sipariş ödeme bekliyor olarak işaretlendi.')
    mark_as_unpaid.short_description = 'Seçili siparişleri ödeme bekliyor olarak işaretle'

