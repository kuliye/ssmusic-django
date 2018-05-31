from django.db import models
from user.models import *
from tinymce.models import HTMLField
from datetime import datetime
class Type(models.Model):
    name=models.CharField(max_length=20)
    pid=models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    typed=models.ForeignKey(Type,on_delete=models.CASCADE)
    info=HTMLField(null=True)
    image=models.ImageField(upload_to='media/album_image/',null=True,default='media/album_image/default.jpg')
    auth=models.CharField(max_length=40,null=True,blank=True)
    isDelete=models.BooleanField(default=False)
    def __str__(self):
        return self.name
class Music(models.Model):
    name=models.CharField(max_length=40)
    info=HTMLField(null=True)
    src=models.FileField(upload_to='static/media/music/')
    click=models.IntegerField(default=0)
    tuijian=models.IntegerField(default=0)
    album=models.ForeignKey(Album,on_delete=models.CASCADE,null=True,blank=True)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.name
class Comment(models.Model):#评论
    owner=models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    music=models.ForeignKey(Music,null=True,blank=True,on_delete=models.CASCADE)
    time=models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
    content=models.CharField(max_length=140)
    pcom=models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    isDelete=models.BooleanField(default=False)
    def __str__(self):
        return self.music.name

class Collection(models.Model):
    user=models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)

class CollDetail(models.Model):
    coll=models.ForeignKey(Collection,on_delete=models.CASCADE)
    music=models.ForeignKey(Music,on_delete=models.CASCADE)
    isDelete=models.BooleanField(default=False)

class History(models.Model):
    user=models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    music=models.ForeignKey(Music,on_delete=models.CASCADE)

class PlayList(models.Model):
    user=models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    music=models.ForeignKey(Music,on_delete=models.CASCADE)












