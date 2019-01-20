import datetime
import uuid                                     # For unique book instances
import re
from django.db import models
from django.utils import timezone
from django.urls import reverse                 # To generate URLS by reversing URL patterns

"""
class SearchManager(models.Manager):
    def search(self, **kwargs):
        qs = self.get_query_set()
        if kwargs.get('q', ''):
            qs = qs.filter(name__icontains=kwargs['q'])
        return qs
"""    

class Passage(models.Model):
    passage_text = models.CharField(max_length = 500)

    def __str__(self):
        return self.passage_text
