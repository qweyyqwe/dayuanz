# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : routing.py
# @Software: PyCharm


from django.urls import path
from social_platform.consumer import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat', ChatConsumer.as_asgi()),
]
