import os
import re
import sys
import subprocess
import datetime
from time import time
from urllib.parse import urlencode
from django.utils import timezone

import json
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core import serializers
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect

from .models import Passage

# ESV API parameters
API_KEY = 'c301f49b5000085fafc0dfb1d696d8855e78a46a'
API_SEARCH_URL = 'https://api.esv.org/v3/passage/search/'
API_TEXT_URL = 'https://api.esv.org/v3/passage/text/'

API_OPTIONS = {
    'include-passage-references': 'false',
    'include-first-verse-numbers': 'false',
    'include-verse-numbers': 'false',
    'include-footnotes': 'false',
    'include-footnote-body': 'false',
    'include-short-copyright': 'false',
    'include-passage-horizontal-lines': 'false',
    'include-heading-horizontal-lines': 'false',
    'include-headings': 'false',
    'include-selahs': 'false',
    'indent-paragraphs': '0',
    'indent-poetry': 'false',
    'indent-poetry-lines': '0',
    'indent-declares': '0',
    'indent-psalm-doxology': '0'
}

# HTTP request headers
ESV_HEADER = 'Authorization: Token %s' % API_KEY
API_HEADERS = {
    'Accept': 'application/json',
    'Authorization': 'Token %s' % API_KEY
}

# Error Handling
class ESVError(Exception):
    def __init__(self, status=200, msg=''):
        self.status = status
        self.msg = msg

class NotFound(ESVError):
    def __str__(self):
        return 'No passage found'

class APIError(ESVError):
    """Raised if API call fails"""

# Views
class IndexView(generic.ListView):
    template_name = 'esvapp/index.html'
    model = Passage
    context_object_name = 'curr_passage_list'
    def get_queryset(self):
        # Return last five questions
        return Passage.objects.all()

class ResultsView(generic.DetailView):
    template_name = 'esvapp/results.html'
    model = Passage

"""
class SearchView(generic.View):

    def get_passage(self,request):
        API_TEXT_URL = 'https://api.esv.org/v3/passage/text/'
        query = request.GET.get('q', '')

        # Combine query and options into GET parameters
        PARAMS = dict(q=query)
        PARAMS.update(API_OPTIONS)
        qs = urlencode(PARAMS)

        # Execute request
        response = requests.get(API_TEXT_URL, params=PARAMS, headers=API_HEADERS)
        try:
            passages = response.json()['passages']
        except (KeyError, Passage.DoesNotExist):
            return render(request, 'esvapp/search.html', context={'search_results': 'No results found'})
        else:
            if passages:
                passage_text = passages[0].strip()
            else:
                passage_text = 'Error: Passage not found'
            #data = json.loads(response)
            #passages = json.dumps(data)
            return render(request, 'esvapp/search.html', context={'passage_list': response},content_type='application/json')
"""

def search_api_search(request):
    template_name = 'esvapp/search.html'
    model = Passage
    query = request.GET.get('q', '')  
    PARAMS = dict(q=query)
    response = requests.get(API_SEARCH_URL, params=PARAMS, headers=API_HEADERS)
    return render(request, template_name, context={"title": "Search Results List", 'passage_list': response},content_type='application/json')

def search_api_text(request):
    template_name = 'esvapp/search.html'
    model = Passage
    query = request.GET.get('q', '')
    # Combine query and options into GET parameters
    PARAMS = dict(q=query)
    PARAMS.update(API_OPTIONS)
    # Execute request
    response = requests.get(API_TEXT_URL, params=PARAMS, headers=API_HEADERS)
    try:
        passages = response.json()['passages']
        ref = response.json()['canonical']
    except (KeyError, Passage.DoesNotExist):
        return render(request, template_name, context={'search_results': 'No results found'})
    else:
        if passages:
            passage_text = passages[0].strip()
            
        else:
            passage_text = 'Error: Passage not found'
        # Render the HTML template search.html with the data in the context variable
        return render(request, template_name, context={'passage_list': response},content_type='application/json')

def search_api(request):
    model = Passage
    query = request.GET.get('q', '')
    if request.method == 'POST':
        user_query = request.POST.get('user_query')
        try:
            reference, passage_obj = get_passage_text(user_query)
             # Render the HTML template results.html with the data in the context variable
            return render(request,'esvapp/results.html', {'reference':reference, 'passage_obj':passage_obj,'user_query':user_query},content_type='application/json')
        except NotFound as e:
            if e.status == 404:
                return render(request, 'esvapp/results.html', {'no_results_found': True})
            else:
                return HttpResponse('ESV API Error', status=e.status) 
    else:
        # Render the HTML template search.html
        return render(request, 'esvapp/search.html',{})

def get_passage_text(user_query):
    # Combine query and options into GET parameters
    PARAMS = dict(q=user_query)
    PARAMS.update(API_OPTIONS)
    # Execute request
    response = requests.get(API_TEXT_URL, params=PARAMS, headers=API_HEADERS)
    passages = response.json()['passages']
    ref = response.json()['canonical']
    if response.status_code == 404:
        raise NotFound(status=404, msg='Error: Passage not found')
    return ref, passages[0].strip() if passages else 'Error: Passage not found'