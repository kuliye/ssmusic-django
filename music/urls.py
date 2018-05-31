from django.urls import path,re_path
from . import views
urlpatterns=[
    path('add_music/',views.add_music),
    path('',views.index),
    path('playlist/',views.playlist),
    re_path(r'^detail(\d+)_info/$',views.detail_info),
    re_path(r'^detail(\d+)_comment(\d+)/$', views.detail_comment),
    re_path(r'^detail(\d+)_album/$', views.detail_album),
    path('reply_handle/' , views.reply_handle),
    path('del_com/',views.del_com),
    path('coll_handle/',views.coll_handle),
    path('playmusic/',views.playmusic),
    path('album/',views.album),
    path('test/', views.test),
    path('player/',views.player),
    path('playlist_delete/',views.playlist_delete),
    path('playmusic/',views.playmusic),
    # path('search/',views.full_search),
    path('found/',views.found),
    re_path(r'^type(\d+)_page(\d+)/$',views.type),

]