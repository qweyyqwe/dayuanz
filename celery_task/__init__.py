# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : __init__.py.py
# @Software: PyCharm
import os
from datetime import timedelta
import django
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_platform.settings")
# sys.path.append("property.settings")
django.setup()


celery_app = Celery('test')
celery_app.config_from_object('celery_task.config')
celery_app.autodiscover_tasks(['celery_task.tasks'])

celery_app.conf.update(
    CELERYBEAT_SCHEDULE={
        'time_task': {
            'task': 'celery_task.tasks.time_task',
            'schedule':  timedelta(seconds=3),
            'args': ()
        },
    }
)
