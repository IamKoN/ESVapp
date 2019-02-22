from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
	path('profile', views.my_profile, name='my_profile'),
	path('signin', views.signin, name='signin'),
	path('signup', views.signup, name='signup')
]

