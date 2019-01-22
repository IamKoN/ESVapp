from django.db import models
from django.urls import reverse
from django.utils import timezone
# Manage database models

class Book(models.Model):
    number = models.PositiveIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('esvapp:books', args=[self.name])

    class Meta:
        ordering = ['number',]


class Chapter(models.Model):
    number = models.PositiveIntegerField(db_index=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
            related_name='chapters')

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse('esvapp:chapters', args=[str(self.number)])

    class Meta:
        ordering = ['number',]
        unique_together=(('book','number',),)


class Verse(models.Model):
    number = models.PositiveIntegerField(db_index=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,
            related_name='verses')
    text = models.TextField()

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse('esvapp:verses', args=[str(self.number)])

    class Meta:
        ordering = ['number',]
        unique_together=(('chapter','number'),)
