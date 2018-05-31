from django.urls import path,re_path
from haystack.views import SearchView

urlpatterns = [
    path('', SearchView()),
]