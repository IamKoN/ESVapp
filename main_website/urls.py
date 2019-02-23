"""
main_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import RedirectView
from esv_search import views


urlpatterns = [
    # path('', views.index, name='home'),
    path('admin/doc/', include('django.contrib.admindocs.urls'), name='docs'),
    path('admin/', admin.site.urls, name='admin'),
    # path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('cart/', include('shopping_cart.urls', namespace='shopping_cart')),
    path('products/', include('products.urls', namespace='products')),
    path('esv_search/', include('esv_search.urls', namespace='esv_search')),
    path('', RedirectView.as_view(url='/', permanent=True))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)