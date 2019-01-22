from django.db import models
from django.urls import reverse

# Manage database models

class Book(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    number = models.IntegerField(unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('esvapp:books', args=[self.name])

    class Meta:
        ordering = ['number',]


class Chapter(models.Model):
    number = models.IntegerField(db_index=True)
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
    number = models.IntegerField(db_index=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,
            related_name='verses')
    text = models.TextField()

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse('esvapp:verses', args=[str(self.number)])

    class Meta:
        ordering = ['number']
        unique_together=(('chapter','number'),)
