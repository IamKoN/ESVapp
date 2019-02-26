from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from search_esv import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/doc/', include('django.contrib.admindocs.urls'), name='docs'),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('allauth.urls')),
    path('accounts_dj/', include('django.contrib.auth.urls')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('cart/', include('shopping_cart.urls', namespace='shopping_cart')),
    path('products/', include('products.urls', namespace='products')),
    path('esv/', include('search_esv.urls', namespace='search_esv')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
