# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : tasks.py
# @Software: PyCharm


import time
from celery_task import celery_app


# @app.task 指定将这个函数的执行交给celery异步执行
@celery_app.task
def test(mobile, code):
    print('1111异步任务')
    print(mobile, code)
    time.sleep(5)
    return mobile + code



@celery_app.task(name='send_email')
def send_email():
    print('发送运输邮件')


@celery_app.task(name='send_email2')
def send_email2():
    print('发送到站邮件')


# 定时任务
@celery_app.task(name='celery_task.tasks.time_task')
def time_task():
    print('定时3秒执行一次')


# 异步任务


from celery import shared_task
@shared_task
def add(x, y):
    return x + y
@shared_task
def mul(x, y):
    return x * y

