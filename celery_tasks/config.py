# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : config.py
# @Software: PyCharm


# 配置信息 key=value
BROKER_URL = "redis://47.111.69.97:6379/9"
CELERY_RESULT_BACKEND = 'redis://47.111.69.97:6379/10'
CELERY_RESULT_SERIALIZER = 'json'   # 结果序列化方案
# 导入指定的任务模块
CELERY_IMPORTS = (
    'celery_tasks.sms.times',
)
