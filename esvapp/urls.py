from django.urls import path

from . import views

# Manage URL patterns

app_name = 'esvapp'

urlpatterns = [
    path('', views.SearchView.as_view(), name='search'),
    path('search/', views.SearchView.as_view(), name='search'),
]
