from django.shortcuts import render,redirect
import json
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.cache import cache
import redis
from .models import *
from user.login_check import login_check
from django.core.paginator import Paginator
from haystack.forms import SearchForm
from django.views.decorators.cache import cache_page

client =  redis.Redis(host='localhost', port=6379, db=0)#创建redis
# Create your views here.
def index(request):#主页
    return render(request,'index.html')

@login_check
def add_music(request):
    musicid=request.GET.get('music_id')
    userid=request.session.get('userid')
    if PlayList.objects.filter(user_id=userid,music_id=musicid).count()!=0:
        PlayList.objects.filter(user_id=userid, music_id=musicid).delete()
    playlist=PlayList()
    playlist.user_id=userid
    playlist.music_id=musicid
    playlist.save()
    return JsonResponse({'data':1})



# def add_music(request):
#     '''添加音乐到播放列表'''
#     musicid=request.GET.get('music_id')
#     userid=request.session.get('userid')
#     music=Music.objects.get(id=musicid,isDelete=False)
#     dict={'id':music.id,'name':music.name,'src':str(music.src)}#创建存储到redis中的字典
#     str1=json.dumps(dict)#将字典对象变为字符串
#     client.zincrby(userid,str1)#存储在有序集合中
#     return JsonResponse({'data':1})

@login_check
def playlist(request):
    userid=request.session.get('userid')
    playlist=PlayList.objects.filter(user_id=userid).order_by('-id')
    context=({'data':playlist})
    return render(request,'music/playlist.html',context)

# def playlist(request):
#     '''播放列表页面'''
#     userid = request.session.get('userid')
#     list=client.zscan_iter(userid)#查询有序集合，键为userid
#     musiclist=[]
#     for item in list:#将查询到的集合，迭代添加进列表中
#         str=json.loads(item[0].decode())#将取出来的字符串变为字典对象
#         musiclist.append(str)
#     context = {'data': musiclist}
#     return render(request,'music/playlist.html',context)


def detail_info(request,musicid):
    userid=request.session.get('userid')
    music = Music.objects.get(id=musicid,isDelete=False)
    album = Album.objects.get(id=music.album_id,isDelete=False)
    collection=Collection.objects.filter(user_id=userid,isDelete=False)
    return render(request, 'music/detail_info.html', {'music': music, 'album': album,'collection':collection})

def detail_comment(request,musicid,pindex):
    music = Music.objects.get(id=musicid,isDelete=False)
    album = Album.objects.get(id=music.album_id,isDelete=False)
    com = Comment.objects.filter(music=music, pcom__isnull=True, isDelete=False).order_by('-id')  # 查询所有该乐曲的父评论，并按照id的倒序进行排序
    ccom = []
    for item in com:
        child = Comment.objects.filter(music=music, pcom=item, isDelete=False).order_by('-id')  # 查询子评论，也按照id的倒序进行排序
        ccom.append({'com': item, 'ccom': child})  # [{'com':父评论1,'ccom':子评论列表1},{'com':父评论2,'ccom':子评论列表2}，...]
    p = Paginator(ccom, 5)
    page = p.page(pindex)
    return render(request, 'music/detail_comment.html', {'music': music, 'album': album, 'com': page, 'paginator': p})

def detail_album(request,musicid):
    music = Music.objects.get(id=musicid,isDelete=False)
    album=Album.objects.get(id=music.album_id,isDelete=False)
    musiclist = Music.objects.filter(album=album,isDelete=False)  # 查找专辑的所有音乐
    return render(request, 'music/detail_album.html', {'music': music, 'album': album, 'musiclist': musiclist})


@login_check
def reply_handle(request):
    '''回复评论'''
    content = request.GET.get('content')
    if len(content)<=5 or len(content)>=140:
        context={'data':2}
    else:
        com_id=request.GET.get('com_id')#父评论的id，如果没有则为空
        music_id=request.GET.get('music_id')
        userid=request.session.get('userid')
        com=Comment()
        com.music_id=music_id
        com.owner_id=userid
        com.pcom_id=com_id
        com.content=content
        com.save()
        if com.pcom_id !=None:
            client.zincrby(str(com.pcom.owner_id)+'com',com.id)#如果评论的父id不为空，则提示父id的用户收到评论信息
        context={'data':1}
    return JsonResponse(context)

@login_check
def del_com(request):
    """删除评论"""
    com_id=request.GET.get('com_id')
    userid = request.session.get('userid')
    com=Comment.objects.get(id=com_id)
    music_id=request.GET.get('music_id')
    if userid==com.owner_id:
        com.isDelete=True#进行逻辑删除
        com.save()
        return redirect('/detail' + music_id + '_2')
    else:
        return redirect('/detail'+music_id+'_2')

@login_check
def coll_handle(request):
    '''收藏音乐'''
    music_id=request.GET.get('musicid')
    collectionid=request.GET.get('collection')#收藏夹的id
    if CollDetail.objects.filter(coll_id=collectionid,music_id=music_id).count()==0:
        coll=CollDetail()
        coll.music_id=music_id#收藏的音乐id
        coll.coll_id=collectionid#收藏夹的id
        coll.save()
        return JsonResponse({'data':1})
    else:
        return JsonResponse({'data':2})


def playmusic(request):
    '''播放音乐'''
    musicid=request.GET.get('musicid')
    music=Music.objects.get(id=musicid,isDelete=False)
    userid = request.session.get('userid')
    music.click+=1#使点击数+1
    music.save()
    if History.objects.filter(music=music,user_id=userid).count()>0:
        History.objects.filter(music=music, user_id=userid).delete()
    history = History()
    history.music = music
    history.user_id = userid  # 添加播放记录
    history.save()
    return JsonResponse({'src':str(music.src)})

def album(request):
    albumid=request.GET.get('albumid')
    album=Album.objects.get(id=albumid,isDelete=False)#查询专辑
    musiclist=Music.objects.filter(album=album,isDelete=False)#查询专辑包含的乐曲
    context={'album':album,'musiclist':musiclist}
    return render(request,'music/album.html',context)

def test(request):
    return render(request,'music/test.html')

def player(request):
    userid = request.session.get('userid')
    musiclist=PlayList.objects.filter(user_id=userid, isDelete=False).order_by('-id')#查询播放列表，按照最新的排序
    context = {'data': musiclist}
    return render(request,'player.html',context)

def playlist_delete(request):
    musicid=request.GET.get('musicid')
    userid=request.session.get('userid')
    PlayList.objects.filter(user_id=userid,music_id=musicid).delete()#删除
    return  JsonResponse({'data':1})

# def full_search(request):
#     keywords=request.GET.get('content')
#     print(keywords)
#     sform = SearchForm(request.GET)
#     posts = sform.search()
#     print(posts)
#
#     return render(request,'music/test.html',{'posts': posts})

@cache_page(60 * 3)
def found(request):
    type = Type.objects.filter(pid__isnull=True)#查询pid为空的类型
    data=[]
    for item in type:
        typed = Type.objects.filter(pid=item)#查找所有子类型
        album = Album.objects.filter(typed__in=typed, isDelete=False).order_by('-id')#按照最新排序查找专辑
        musiclist=Music.objects.filter(album__in=album, isDelete=False).order_by('-click')[0:5]#查找点击量最高的音乐
        data.append({'type':item,'musiclist':musiclist,'album':album,'typed':typed})#将所有查询列表放入data列表中
    return render(request,'music/found.html',{'data':data})

@cache_page(60 * 3)
def type(request,typeid,pindex):
    type=Type.objects.get(id=typeid)
    if type.pid is None:#如果类型的pid为空，则说明该类型是父类型
        typed = Type.objects.filter(pid=type)#查询父类型包含的所有子类型
        album1 = Album.objects.filter(typed__in=typed, isDelete=False)#查找专辑类型属于子类型的专辑
    else:#如果为子类型
        album1=type.album_set.all()#反向查找，根据类型查找对应类型的专辑
    album = []
    for item in album1:
        music = Music.objects.filter(album=item, isDelete=False)
        album.append({'album': item, 'music': music})#查询的所有结果放入album列表中
    p = Paginator(album, 3)
    page = p.page(pindex)
    context = {'type': type, 'album': page, 'paginator': p}
    return render(request,'music/type.html',context)