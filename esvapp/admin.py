from django.contrib import admin

from .models import Book, Chapter, Verse

# Register models

admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Verse)