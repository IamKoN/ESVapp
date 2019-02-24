from django.urls import path

from . import views

app_name = 'search_esv'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.SearchView.as_view(), name='search')
]
