# -*- coding: utf-8 -*-
from django.contrib import admin
from blog.models import User
from kombu.transport.django import models as kombu_models


# class ButhorAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',)
#     search_fields = ('id','name',)
#     #list_filter = ('name',)
#     ordering =('id',)
#     fields = ('id', 'sex')



admin.site.register(kombu_models.Message)
# Register your models here.
# admin.site.register(Student)
# admin.site.register(Teacher)
admin.site.register(User)

