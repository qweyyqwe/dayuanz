# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : times.py
# @Software: PyCharm

from celery_tasks.main import celery_app


@celery_app.task(name='celery_tasks.sms.times.my_times')
def my_times(x, y):
    print(x, y)
    return x + y


@celery_app.task(name='celery_tasks.sms.times.my_times2')
def my_times2():
    print('哈哈哈哈')


