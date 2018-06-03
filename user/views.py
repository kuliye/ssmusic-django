from django.http import HttpRequest,HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.core.mail import send_mail
import random
from .models import *
from hashlib import sha1
import os
import redis
from django.conf import settings
from music.models import *
from django.core.paginator import Paginator
from .login_check import *
from django.views.decorators.cache import cache_page
import os
import time
client =  redis.Redis(host='localhost', port=6379, db=0)


def register(request):
    '''注册页面'''
    return render(request, 'user/register.html')


def register_handle(request):
    '''注册处理'''
    userinfo=UserInfo()
    uname=request.POST.get('uname')
    uemail=request.POST.get('uemail')
    upwd=request.POST.get('upwd')
    cupwd=request.POST.get('cupwd')
    cnumber=request.POST.get('cnumber')#用户所填写的验证码
    check_num=request.session['check_num']#生成的邮箱验证码
    if cnumber==check_num:
        if upwd==cupwd:
            sh=sha1()
            sh.update(upwd.encode('utf-8'))
            userinfo.upwd=sh.hexdigest()
            userinfo.uname=uname
            userinfo.uemail=uemail
            userinfo.save()
            return render(request,'user/login.html')
        else:
            return redirect(request,'user/register.html',{'info':'两次密码不一致'})
    else:
        return redirect(request, 'user/register.html', {'info':'验证码不正确'})


def sendmail(request):
    '''发送验证邮件'''
    check_num = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
        random.randint(0, 9))
    uemail=request.GET.get('uemail')
    send_mail('SMUSIC', '欢迎注册SM，你的验证码为' + check_num+'，有效时间为5分钟，请尽快填写', 'niaohai1@163.com', [uemail], fail_silently=True)
    request.session['check_num'] = check_num
    request.session.set_expiry(300)#设置过期时间
    return JsonResponse({'check_num': check_num})

def name_exist(request):
    '''判断用户名是否已经存在'''
    username=request.GET.get('username')
    if len(UserInfo.objects.filter(uname=username))!=0:#查询用户名是否存在
        return JsonResponse({'result':1})
    else:
        return JsonResponse({'result':0})

def login(request):
    '''登陆页面'''
    return render(request,'user/login.html')


def logout(request):
    '''登出'''
    request.session.flush()
    return render(request,'index.html')


def login_handle(request):
    '''登陆处理'''
    uname=request.POST.get('uname')
    upwd=request.POST.get('upwd')
    sh=sha1()
    sh.update(upwd.encode('utf-8'))
    if UserInfo.objects.filter(uname=uname).exists():
        userinfo=UserInfo.objects.get(uname=uname)
        if userinfo.upwd==sh.hexdigest():#如果加密后的密码与数据库相同
            request.session['username']=userinfo.uname
            request.session['useremail']=userinfo.uemail
            request.session['userphoto']=str(userinfo.uphoto)
            request.session['userid']=userinfo.id
            url=request.COOKIES.get('url','')#获取登录前的地址，如果登陆成功则跳转回原来的地址
            red=JsonResponse({'data':1,'url':url})
            return red
        else:
            return JsonResponse({'data':0})
    else:
        return JsonResponse({'data':0})

@login_check
def user_info(request):
    '''用户信息页面'''
    userid=request.session.get('userid')
    historylist=History.objects.filter(user_id=userid).order_by('-id')[0:5]#查询播放历史
    context={'historylist':historylist}
    return render(request,'user/user_info.html',context)

@login_check
def user_notice(request):
    '''用户消息页面'''
    userid=request.session.get("userid")
    list = client.zscan_iter(str(userid)+'com')#读取redis中的回复消息
    notice=[]
    for item in list:
        com=Comment.objects.get(id=item[0].decode())#将数据存储为列表格式
        notice.append(com)
    context={'notice':notice}
    return render(request,'user/user_notice.html',context)

@login_check
def user_update(request,index):
    '''用户上传页面'''
    type=Type.objects.filter(pid__isnull=True)
    album1=Album.objects.filter(owner_id=request.session.get('userid'),isDelete=False)#查询专辑信息
    album=[]
    for item in album1:
        music=Music.objects.filter(album=item,isDelete=False)#将专辑信息存储在列表中
        album.append({'album':item,'music':music})#[{'album':album,'musiclist':musiclist},{'album':album,'musiclist':musiclist},....]
    p=Paginator(album,3)#进行分页处理
    page=p.page(index)
    context={'type':type,'album':page,'paginator':p}
    return render(request,'user/user_update.html',context)

@login_check
def user_coll(request):
    '''查找用户收藏'''
    userid=request.session.get('userid')
    collection=Collection.objects.filter(user_id=userid,isDelete=False)#查找收藏
    coll=[]
    for item in collection:
        musiclist=CollDetail.objects.filter(coll=item,isDelete=False)#将收藏信息存储在列表中
        coll.append({'collection':item,'coll':musiclist})#[{'coll':item,'col':music},{'coll':item,'col':music},{'coll':item,'col':music}...]
    context={'data':coll}
    return render(request,'user/user_coll.html',context)

@login_check
def upload(request):
    """上传头像"""
    s = request.FILES['pic1']
    fmat=['.gif','.jpg','.png','.jpeg']#支持图片的格式
    if os.path.splitext(s.name)[1] in fmat:#如果符合图片格式
        username = request.session.get('username')
        userinfo = UserInfo.objects.get(uname=username)
        filename=str(userinfo.id)+str(int(time.time()))+os.path.splitext(s.name)[1]#用用户id加时间命名，防止重复
        pic = os.path.join(settings.MEDIA_PHOTO,filename)
        userinfo.uphoto='/static/media/user_photo/'+filename#存储目录
        with open(pic, 'wb') as pic:
            for c in s.chunks():
                pic.write(c)
        userinfo.save()
        request.session['userphoto'] = str(userinfo.uphoto)
        return render(request,'user/user_info.html',{'erro':0})#r如果图片符合格式返回0
    return render(request,'user/user_info.html',{'erro':1})#如果图片不符合格式返回错误信息

@login_check
def type_select(request):
    '''选择专辑类型'''
    typename=request.GET.get('type')
    ptype=Type.objects.get(name=typename)
    type=Type.objects.filter(pid=ptype)
    typed=[]
    for item in type:
        typed.append({'id':item.id,'name':item.name})
    return JsonResponse({'typed':typed})

@login_check
def album_handle(request):
    '''创建专辑'''
    name=request.POST.get('a_name')
    typename=request.POST.get('type')
    auth=request.POST.get('a_auth')
    if len(name)&len(typename)!=0:#如果填写的专辑名称和类型名称都不为空
        type=Type.objects.get(name=typename)
        album=Album()
        album.name=name
        album.typed=type
        userid=request.session.get('userid')
        album.owner_id=userid
        album.auth=auth
        s = request.FILES['pic2']
        username = request.session.get('username')
        userinfo = UserInfo.objects.get(uname=username)
        albumpic=str(userinfo.id) + str(int(time.time())) + os.path.splitext(s.name)[1]#专辑的封面
        pic = os.path.join(settings.MEDIA_ALBUM, albumpic)
        with open(pic, 'wb') as pic:
            for c in s.chunks():
                pic.write(c)
        album.image = '/static/media/album_image/' + albumpic

        album.save()
        return redirect('/user/user_update1/')
    else:
        return redirect('/user/user_update1/')

@login_check
def music_handle(request):
    '''上传音乐'''
    m_album=request.POST.get('m_album')
    m_name=request.POST.get('m_name')
    m_info=request.POST.get('m_info')
    m_src=request.FILES['m_src']
    username = request.session.get('username')
    userinfo = UserInfo.objects.get(uname=username)
    musicname = str(userinfo.id) + str(int(time.time())) + os.path.splitext(m_src.name)[1]  # 用用户id加时间命名，防止重复
    path=os.path.join(settings.MEDIA_MUSIC,musicname)
    with open(path,'wb') as p:
        for c in m_src.chunks():
            p.write(c)
    music=Music()
    music.name=m_name
    music.src='/static/media/music/'+musicname
    music.info=m_info
    music.album_id=m_album
    music.type=music.album.typed.pid
    music.save()
    return redirect('/user/user_update1/')

@login_check
def coll_create(request):
    '''创建收藏夹'''
    userid=request.session.get('userid')
    name=request.GET.get('c_name')
    coll=Collection()
    coll.name=name
    coll.user_id=userid
    coll.save()
    return redirect('/user/user_coll')

@login_check
def coll_delete(request):
    '''删除收藏'''
    collid=request.GET.get('collid')
    coll=Collection.objects.get(id=collid).delete()
    coll.save()
    return JsonResponse({'data':1})

@login_check
def coll_delete_detail(request):
    '''收藏详细列表'''
    colldeid=request.GET.get('colldeid')
    collde=CollDetail.objects.get(id=colldeid)
    collde.isDelete=True
    collde.save()
    return JsonResponse({'data':1})

@login_check
def delete_album(request):
    '''删除已经上传的专辑'''
    albumid=request.GET.get('albumid')
    album=Album.objects.get(id=albumid)
    album.isDelete=True
    album.save()
    return JsonResponse({'data':1})

@login_check
def delete_album_detail(request):
    '''删除专辑内单个音乐'''
    musicid=request.GET.get('musicid')
    music=Music.objects.get(id=musicid,isDelete=False)
    music.isDelete=True
    music.save()
    return JsonResponse({'data':1})
