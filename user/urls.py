from django.urls import path,re_path
from . import views
urlpatterns=[
    path('register/',views.register),
    path('register_handle/',views.register_handle),
    path('sendmail/',views.sendmail),
    path('name_exist/',views.name_exist),
    path('login/',views.login),
    path('login_handle/',views.login_handle),
    path('user_info/',views.user_info),
    path('user_notice/',views.user_notice),
    re_path(r'^user_update(\d+)/$',views.user_update),
    path('upload/',views.upload),
    path('type_select/',views.type_select),
    path('album_handle/',views.album_handle),
    path('music_update/',views.music_handle),
    path('logout/',views.logout),
    path('user_coll/',views.user_coll),
    path('coll_create/',views.coll_create),
    path('coll_delete/',views.coll_delete),
    path('coll_delete_detail/',views.coll_delete_detail),
    path('delete_album/',views.delete_album),
    path('delete_album_detail/',views.delete_album_detail),
]