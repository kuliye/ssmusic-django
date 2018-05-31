# coding=utf-8
from haystack import indexes
from .models import Music,Album
class MusicIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)
    def get_model(self):
        return Music
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
