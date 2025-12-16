from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:category_type>/', views.category_products, name='category_products'),
    path('p/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/', views.order_success, name='order_success'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('about/', views.about, name='about'),
    # Auth URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    # User URLs
    path('orders/', views.order_history, name='order_history'),
]
