from django.db import models

# Manage database models

"""
class SearchManager(models.Manager):
    def search(self, **kwargs):
        qs = self.get_query_set()
        if kwargs.get('q', ''):
            qs = qs.filter(name__icontains=kwargs['q'])
        return qs
"""    

class Book(models.Model):
    book_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.book_name

class Chapter(models.Model):
    chapter_num = models.IntegerField

    def __str__(self):
        return self.chapter_num

class Verse(models.Model):
    verse_num = models.IntegerField

    def __str__(self):
        return self.verse_num
