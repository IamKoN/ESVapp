import requests

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

# Views

def home(request):
    return render(request, 'home/index.html')
