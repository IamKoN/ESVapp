import requests

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from mysite.settings import API_HEADERS, API_OPTIONS, API_SEARCH_URL, API_TEXT_URL
from .models import Book, Chapter, Verse

# Views
def index(request):
    return render(request, 'esvapp/index.html')


class SearchView(generic.View):
    # context_object_name = 
    template_name ='esvapp/search.html'


    def post(self,request):
        user_query = request.POST.get('q', '')
        try:
            text_obj = get_passage_text(user_query)
            search_obj = get_passage_search(user_query)
            context = {
                'no_results_found': False,
                'user_query': user_query,
                'total_pages': search_obj['total_pages'],
                'page': search_obj['page'],
                'total_results': search_obj['total_results'],
                'reference': text_obj['canonical'],
                'passages': text_obj['passages'],
            }
            all_results = search_obj['results']
            for result in all_results:
                context.update(new_cont=result['content'], new_ref=result['reference'])
            
            return render(request, 'esvapp/results.html', context=context)
        except NotFound as e:
            if e.status == 404:
                return render(request, 'esvapp/results.html', {'no_results_found': True, 'error_msg': e.msg})
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
    template_name = 'esvapp/book_list.html'
    model = Book
    context_object_name = 'curr_book_list'

    def get_queryset(self):
        return Book.objects.all()


class ChapterList(generic.ListView):
    template_name = 'esvapp/chap_list.html'
    model = Chapter
    context_object_name = 'curr_chapter_list'

    def get_queryset(self):
        return Chapter.objects.all()


class VerseList(generic.ListView):
    template_name = 'esvapp/verse_list.html'
    model = Verse
    context_object_name = 'curr_verse_list'

    def get_queryset(self):
        return Verse.objects.all()
        #return Verse.objects.filter(pk=Verse.number)

    def get(self, request):
        verse_num = request.GET.get('vn', 1)
        try:
            text_obj = get_passage_text(verse_num)

            context = {
                'user_query': text,
                'verse_num': verse_num,
                'book_name': text_obj['canonical'].split()[0],
                'reference': text_obj['canonical'],
                'passages': text_obj['passages'],
            }
            return render(request, 'esvapp/verse_detail.html', context=context)
        except NotFound as e:
            if e.status == 404:
                return render(request, 'esvapp/verses.html', {'no_results_found': True, 'error_msg': e.msg})
            else:
                return HttpResponse('ESV API Error', status=e.status) 
  


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
