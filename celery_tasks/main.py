# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : main.py
# @Software: PyCharm


import os
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_platform.settings')
# 创建celery实例

from celery import Celery
celery_app = Celery('mycelery')


# 配置redis的url
celery_app.config_from_object('celery_tasks.config')

# 配置执行的文件夹
celery_app.autodiscover_tasks(['celery_tasks.sms.times'])

celery_app.conf.update(
    CELERYBEAT_SCHEDULE={
        'sum-task': {
            'task': 'celery_tasks.sms.times.my_times',  # 这里是要执行的路径
            'schedule': timedelta(seconds=5),  # 时间，每隔几秒执行一次
            'args': (5, 6)  # 随意定的参数
        },

        'sum-task1': {
            'task': 'celery_tasks.sms.times.my_times2',
            'schedule': timedelta(seconds=3),
            'args': ()
        },
    }
)
