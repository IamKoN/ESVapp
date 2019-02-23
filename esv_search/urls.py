from django.urls import path

from . import views

app_name = 'esv_search'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.SearchView.as_view(), name='search')
]
