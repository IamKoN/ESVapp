
import datetime
import json
import os
import re
import subprocess
import sys
import requests

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core import serializers
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render
#from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#from django.contrib.auth.decorators import permission_required


from .models import Choice, Question, Passage
#####################################################################################

from __future__ import print_function
from hashlib import md5
from time import time
from urllib.parse import urlencode

API_KEY = 'c301f49b5000085fafc0dfb1d696d8855e78a46a'
#API_KEY = '{{5974948d3baa3d1cabc4eb00e4099e3d785d43df}}'
API_URL = 'https://api.esv.org/v3/passage/text/'

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
API_HEADERS = {
    'Accept': 'application/json',
    'Authorization': 'Token %s' % API_KEY,
}

class ESVError(Exception):
    """Base error class"""

class APIError(ESVError):
    """Raised if API call fails"""

class NotFound(ESVError):
    """Raised if no passage found"""
    def __str__(self):
        return 'No passage found'
  
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return last five questions """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """ Excludes any questions that aren't published yet """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Return HttpResponseRedirect after successfully dealing with POST data
        # to prevent data from being posted twice if a user hits the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def fetch_url(url, params, headers):
    """Fetch a URL using cURL and parse response as JSON.
    Args:
        url (str): Base URL without GET parameters.
        params (dict): GET parameters.
        headers (dict): HTTP headers.
    Returns:
        object: Deserialised HTTP JSON response.
    Raises:
        APIError: Raised if API returns an error.
    """
    # Encode GET parameters and add to URL
    qs = urlencode(params)
    url = url + '?' + qs

    # Build cURL command
    cmd = ['/usr/bin/curl', '-sSL', url]
    for k, v in headers.items(): cmd.extend(['-H', '{}: {}'.format(k, v)])

    # Run command and parse response
    output = subprocess.check_output(cmd)
    data = json.loads(output)
    if 'detail' in data: raise APIError(data['detail'])
    return data

def exit_with_error(title, err, tb=False):
    """
    Show an error message in Alfred and exit script.
    Args:
        title (unicode): Title of item.
        err (Exception): Error whose message to show as item subtitle.
    """
    output = {'items': [{'title': title, 'subtitle': str(err)}]}
    json.dump(output, sys.stdout)
    sys.exit(1)  # 1 indicates something went wrong

def search(request):
    """
    Perform ESV API query
    Args: query (unicode): Search string.
    Returns Passage: Passage from API
    """
    query = request.GET.get('query')
    queryset = Passage.objects.filter(name__istartswith= query)

    # can also display data on index.html
    context = {
        "title": "Passage List",
        "objects": queryset
    }
    serialized_queryse = serializers.serialize('json', queryset)
    # create json file
    with open('data.json', 'w') as outfile:
        json.dump(serialized_queryse, outfile)

    # Combine query and options into GET parameters
    params = dict(q=query.encode('utf-8'))
    params.update(API_OPTIONS)

    # Execute request
    data = fetch_url(API_URL, params, API_HEADERS)
    passage = Passage.from_response(data)

    # Render the HTML template index.html with the data in the context variable.
    #return render(request,'polls/index.html', context=context,)

    # display data at http://127.0.0.1:8000/
    #return HttpResponse(serialized_queryse, content_type='application/json')
    return HttpResponse(passage, content_type='application/json')
