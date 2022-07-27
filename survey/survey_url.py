# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : plaza_url.py
# @Software: PyCharm


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('show_question_answer/', views.ShowQuestionAnswer.as_view()),
    # 管理员增删改查调查以及选项
    path('add_question_answer/', views.AddQuestionAnswer.as_view()),
    path('update_question_answer/', views.UpdateQuestionAnswer.as_view()),
    path('del_question_answer/', views.DelQuestionAnswer.as_view()),



]

