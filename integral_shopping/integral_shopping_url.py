# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : f_circle.py
# @Software: PyCharm


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add_integral_shopping/', views.AddIntegralShopping.as_view()),
    # 展示所有商品
    path('get_all_shopping/', views.GetAllIntegralShopping.as_view()),
    path('get_one_shopping/', views.GetOneIntegralShopping.as_view()),
    # 修改商品
    path('update_one_shopping/', views.UpdateIntegralShopping.as_view()),
    # 将商品下架
    path('del_shopping/', views.DelIntegralShopping.as_view()),

    path('max_sale_count/', views.MaxSaleCount.as_view()),
]
