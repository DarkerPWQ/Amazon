# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    desc = models.TextField()
class Loginuser(models.Model):

    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    #shunxu = models.IntegerField(null=True)
    email = models.CharField(max_length=40,blank=True,null=True)
    class Meta:
        db_table = 'loginuser'
class use_upfile(models.Model):#上传下载标志
    loginuser = models.ForeignKey(Loginuser)
    filepath =  models.CharField(max_length=200)
    fileflag = models.IntegerField(max_length=50)
    upload = models.CharField(max_length=50)
    def __unicode__(self):
        return self.loginuse
class Display(models.Model):
    loginuser = models.ForeignKey(Loginuser)
    Asin = models.CharField(max_length=100,blank=True)
    productname = models.CharField(max_length=255,blank=True)
    productkeyword1 = models.CharField(max_length=200,blank=True)
    productkeyword2 = models.CharField(max_length=200,blank=True)
    productkeyword3 = models.CharField(max_length=200,blank=True)
    country = models.CharField(max_length=20,blank=True)
    countryname = models.CharField(max_length=100,blank=True)
    def __unicode__(self):
        return self.loginuser

class Queryproducts(models.Model):#查询记录
    loginuser = models.ForeignKey(Loginuser)
    Asin = models.CharField(max_length=100,blank=True,null=True)
    productname = models.CharField(max_length=255)
    productkeyword1 = models.CharField(max_length=200,blank=True)
    productrank1 = models.CharField(max_length=200,blank=True)
    productindex1 = models.CharField(max_length=20,blank=True,null=True)
    varyindex1 = models.CharField(max_length=200,blank=True)
    pic1 = models.CharField(max_length=200,blank=True,null=True)
    flag1 = models.IntegerField(blank=True,null=True)
    productkeyword2 = models.CharField(max_length=200,blank=True)
    productrank2 = models.CharField(max_length=200,blank=True)
    productindex2 = models.CharField(max_length=20,blank=True,null=True)
    varyindex2 = models.CharField(max_length=200,blank=True)
    pic2 = models.CharField(max_length=200,blank=True)
    flag2 = models.IntegerField(blank=True,null=True)
    productkeyword3 = models.CharField(max_length=200)
    productrank3 = models.CharField(max_length=200,blank=True)
    productindex3 = models.CharField(max_length=20,blank=True,null=True)
    varyindex3 = models.CharField(max_length=200,blank=True)
    pic3 = models.CharField(max_length=200,blank=True)
    flag3 = models.IntegerField(blank=True,null=True)
    querytime = models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=20,blank=True)
    countryname = models.CharField(max_length=100,blank=True)
    class Meta:
        db_table = 'queryproducts'
    def __unicode__(self):
        return self.productname

# class Teacher(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=10)
#     class Meta:
#         db_table = 'teacher'
#         permissions = (('can_view1','can see1'),
#         ('can_add1','can see2'),
#         ('can_edit1','can see3'),
#         ('can_del','can see4'))
class User111(models.Model):
    #username = models.CharField(max_length = 30)
    headImg = models.FileField(upload_to = './upload/')#用户存放上传文件的路径。

    def __unicode__(self):
        return self.username
