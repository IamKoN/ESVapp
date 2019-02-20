import requests

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from main_website.settings import API_HEADERS, API_OPTIONS, API_SEARCH_URL, API_TEXT_URL


# Views

class SearchView(generic.View):

    def get(self, request):
        user_query = request.GET.get('q', ' ')
        page_num = request.GET.get('page', '1')
        page_size = request.GET.get('page-size', '20')
        try:
            text_obj = get_passage_text(user_query)
            search_obj = get_passage_search(user_query, page_num, page_size)
            all_pages = []
            for i in range(search_obj['total_pages']):
                all_pages.append(i)
            context = {
                    'no_results_found': True,
            }
            if search_obj['results']:
                context = {
                    'no_results_found': False,
                    'user_query': user_query,
                    'total_pages': search_obj['total_pages'],
                    'all_pages': all_pages,
                    'page': search_obj['page'],
                    'total_results': search_obj['total_results'],
                    'all_results': search_obj['results'],
                    'page_size': page_size,

                }
            elif text_obj['passages']:
                context = {
                    'no_results_found': False,
                    'reference': text_obj['canonical'],
                    'passages': text_obj['passages'][0].strip(),
                }
            else:
                raise NotFound(status=404, msg='Error: Passage not found')
            return render(request, 'esv_search/results.html', context=context)
        except NotFound as e:
            if e.status == 404:
                return render(request, 'esv_search/results.html', {'error_msg': e.msg})
            else:
                return HttpResponse('ESV API Error', status=e.status) 
    
    def post(self, request):
        return render(request, 'base.html', {})


def get_passage_search(user_query, page_num, page_size):
    request_params = {
        'q': user_query,
        'page':page_num,
        'page-size':page_size,
    }

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
