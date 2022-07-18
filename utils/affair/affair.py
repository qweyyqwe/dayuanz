# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : affair.py
# @Software: PyCharm


from django.db import transaction


# # 装饰器用法
# @transaction.atomic
# def viewfunc(request):
#     # 这些代码会在一个事务中执行
#     pass


# # with上下文管理
# def viewfunc(request):
#     # 这部分代码不在事务中，会被 Django 自动提交
#
#     with transaction.atomic():
#         # 这部分代码会在事务中执行
#         pass
