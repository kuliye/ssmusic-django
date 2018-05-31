from django.db import models

# Create your models here.

class UserInfo(models.Model):
    uname=models.CharField(max_length=20)
    uemail=models.CharField(max_length=30)
    upwd=models.CharField(max_length=40)
    uphoto=models.ImageField(upload_to='media/user_info/',null=True,default='/static/media/user_info/default.jpg')
    def __str__(self):
        return self.uname
