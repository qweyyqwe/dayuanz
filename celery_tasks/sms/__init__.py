# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : __init__.py.py
# @Software: PyCharm



#1.为celery的运行  设置Django环境
import os
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_platform.settings')
