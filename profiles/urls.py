from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
	path('order_history', views.my_profile, name='my_profile'),
	path('signin', views.SignInView.as_view(), name='signin'),
	path('signup', views.signup, name='signup'),
	path('reset_password', views.password_reset, name='password_reset'),
]
