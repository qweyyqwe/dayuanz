# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : plaza_url.py
# @Software: PyCharm


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # 签到奖励表
    path('reward_list/', views.GetRewardList.as_view()),
    # 获取当前签到数据
    path('get_user_sign_info/', views.GetUserSignInfo.as_view()),

    path('sign/', views.SignServer.as_view()),



]

