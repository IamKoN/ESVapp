from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('order_history', views.my_profile, name='my_profile'),
]
