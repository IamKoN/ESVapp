from django.urls import path

from . import views

# Manage URL patterns

app_name = 'esvapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('search_test/', views.search_api_search, name='search_test'),
    path('esvbible/', views.BookList.as_view(), name='books'),
    path('esvbible/<str:book>/', views.ChapterList.as_view(), name='chapters'),
    path('esvbible/<str:book>/<int:chapter>/', views.VerseList.as_view(), name='verses'),
    path('esvbible/<str:book>/<int:chapter>/<int:verse>/', views.VerseDetail.as_view(), name='verse_detail'),
]
