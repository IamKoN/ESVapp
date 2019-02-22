from django.urls import path

from . import views

app_name = 'esv_search'

urlpatterns = [
    path('', views.SearchView.as_view(), name='search')
]
