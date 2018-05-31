from django.contrib import admin
from .models import *
class MusicAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Type)
admin.site.register(Music,MusicAdmin)
admin.site.register(Album)
admin.site.register(Comment)
# Register your models here.
