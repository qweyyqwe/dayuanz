# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : plaza_url.py
# @Software: PyCharm


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # 发布站内信
    path('add_mail/', views.AddMail.as_view()),
    # 展示用户站内信
    path('get_mail/', views.GetMail.as_view()),



]

