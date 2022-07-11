# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : f_circle.py
# @Software: PyCharm


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add_circle/', views.AddCircle.as_view())
]
