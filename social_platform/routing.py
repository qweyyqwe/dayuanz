# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : routing.py
# @Software: PyCharm


from django.urls import path, re_path
from social_platform.consumer import ChatConsumer

websocket_urlpatterns = [
    # path('ws/chat', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<user_id>\w+)$', ChatConsumer.as_asgi()),
]
