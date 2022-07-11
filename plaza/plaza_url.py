# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : plaza_url.py
# @Software: PyCharm


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # 发布动态
    path('add_plaza/', views.AddPlaza.as_view()),
    # 所有动态
    path('all_plaza/', views.AllPlaza.as_view()),
    path('add_discuss/', views.AddDiscuss.as_view()),
    # 获取评论
    path('get_all_discuss/', views.GetDiscuss.as_view()),
    # 获取七牛云token
    path('get_qiniu/', views.Qiniuyun.as_view()),
    # 审核列表
    # path('get_qiniu/', views.Qiniuyun.as_view()),
    # 审核人需审核的列表
    path('reviewer_list/', views.ReviewerList.as_view()),
    # 审核员操作
    path('reviewer_plaza/', views.CheckPlaza.as_view()),



]

