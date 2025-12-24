from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from store.sitemaps import ProductSitemap, CategorySitemap, StaticViewSitemap
from store import views as store_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('healthz', store_views.healthz, name='healthz'),
    path('sitemap.xml', sitemap, {'sitemaps': {
        'products': ProductSitemap,
        'categories': CategorySitemap,
        'static': StaticViewSitemap,
    }}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

# Custom error handlers
handler404 = 'store.views.custom_404'
handler500 = 'store.views.custom_500'

# Serve media files even when DEBUG=False (low-traffic/simple deployment on Render)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
