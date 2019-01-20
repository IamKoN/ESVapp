from django.urls import path

from . import views

app_name = 'esvapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #path('', views.search_api_text, name='index'),
    path('search/', views.search_api_text, name='search'),
    path('search_test/', views.search_api_search, name='search_test'),
    path('search/<str:user_query>/', views.ResultsView.as_view(), name='results'),
    #path('search_view/', views.SearchView.as_view(), name='search_view'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
]
