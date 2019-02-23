import requests

from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404, render
from django.views import generic


from shopping_cart.models import Order
from .models import Profile


# Views
# ======================================================================
class SignInView(generic.View):

	def get(self, request):
		email = request.GET.get('email', 'email@example.com')
		return render(request, "profiles/signin.html")

	def post(self, request):
		email = request.POST.get('email', 'email@example.com')
		password = request.POST.get('password', ' ')
		user = authenticate(request, username=email, password=password)
		if user is not None:
			login(request, user)
			return render(request, "profiles/profile.html")
		else:
			# Return an 'invalid login' error message.
			return render(request, "profiles/signin.html")


def my_profile(request):
	my_user_profile = Profile.objects.filter(user=request.user).first()
	my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
	context = {
		'my_orders': my_orders
	}
	return render(request, "profiles/order_history.html", context)

def signin(request):
	email = request.POST['email']
	password = request.POST['password']
	user = authenticate(request, username=email, password=password)
	if user is not None:
		login(request, user)
		return render(request, "profiles/profile.html")
	else:
		# Return an 'invalid login' error message.
		return render(request, "profiles/signin.html")

	
def signup(request):
	# Create user and save to the database
	un = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	user = User.objects.create_user(un, email, password)

	# Update fields and then save again
	user.save()

	return render(request, "profiles/signup.html")


def logout_view(request):
    logout(request)
    # Redirect to a success page.