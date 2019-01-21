import json
import requests

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views import View

from mysite.settings import API_HEADERS, API_OPTIONS, API_SEARCH_URL, API_TEXT_URL
from .models import Book, Chapter, Verse

# Views
def index(request):
    return render(request, 'esvapp/index.html')

class SearchView(generic.View):
    #context_object_name = 
    template_name ='esvapp/search.html'

    def post(self,request):
        user_query = request.POST.get('q', 'default_value')
        user_query2 = request.GET.get('q', 'default_value')
        try:
            text_obj = get_passage_text(user_query)
            search_obj = get_passage_search(user_query)
            context = {
                'no_results_found': False,
                'user_query': user_query,
                #'user_query': text_obj['query'],
                'total_pages': search_obj['total_pages'],
                'page': search_obj['page'],
                'total_results' : search_obj['total_results'],
                'all_results' : search_obj['results'],
                'reference': text_obj['canonical'],
                'passages': text_obj['passages'],
            }
            return render(request,'esvapp/results.html', context=context)
        except NotFound as e:
            if e.status == 404:
                return render(request, 'esvapp/results.html', {'no_results_found': True})
            else:
                return HttpResponse('ESV API Error', status=e.status) 
    
    def get(self,request):
        return render(request, 'esvapp/search.html',{})
    
def get_passage_search(user_query):
    request_params = dict(q=user_query)
    response = requests.get(API_SEARCH_URL, params=request_params, headers=API_HEADERS)
    if response.status_code == 404:
        raise NotFound(status=404, msg='Error: Results not found')
    return response.json()

def get_passage_text(user_query):
    request_params = dict(q=user_query)
    request_params.update(API_OPTIONS)
    response = requests.get(API_TEXT_URL, params=request_params, headers=API_HEADERS)
    if response.status_code == 404:
        raise NotFound(status=404, msg='Error: Passage not found')
    return response.json()

class BookList(generic.ListView):
    template_name = 'esvapp/base.html'
    model = Book

class ChapterList(generic.ListView):
    template_name = 'esvapp/base.html'
    model = Chapter

class VerseList(generic.ListView):
    template_name = 'esvapp/base.html'
    model = Verse

class VerseDetail(generic.DetailView):
    template_name = 'esvapp/base.html'

    #def get_queryset(self):
    #    return Verse.objects.filter(pk=verse_id)

# Error Handling
class ESVError(Exception):
    def __init__(self, status=200, msg=''):
        self.status = status
        self.msg = msg

class NotFound(ESVError):
    def __str__(self):
        return 'Passage not found'

class APIError(ESVError):
    def __str__(self):
        return 'ESV API error'