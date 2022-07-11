# -*- coding: utf-8 -*-
# @Time    : 2021/11/22
# @File    : consumer.py
# @Software: PyCharm


# 单回话
"""

import json

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

CONN_LIST = []


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print("开始链接...")
        # 有客户端来向后端发送websocket连接的请求时，自动触发。
        # 服务端允许和客户端创建连接（握手）。
        self.accept()

        CONN_LIST.append(self)

    def websocket_receive(self, message):
        # 浏览器基于websocket向后端发送数据，自动触发接收消息。
        print('接受的消息', message)
        text = message['text']  # {'type': 'websocket.receive', 'text': '阿斯蒂芬'}
        print("接收到消息-->", text)
        res = {'result': 'ok'}
        for conn in CONN_LIST:
            conn.send(json.dumps(res))

    def websocket_disconnect(self, message):
        CONN_LIST.remove(self)
        raise StopConsumer()
"""

import json

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

CONN_LIST = []


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 接收这个客户端的连接
        print("1111111111111111收到建立连接请求", message)
        self.accept()
        # async_to_sync(self.channel_layer.group_add)('1314', self.channel_name)

    # def websocket_receive(self, message):
    #     print("2222222222222222接收到消息-->", message)
    #     data = json.loads(message['text'])
    #     print('>>>>>>>>data', data)
    #     chat_type = data.get('chat_type')
    #     chat_id = data.get('chat_id')
    #     chat_content = data.get('message')
    #     if chat_type == "add_chat":
    #         async_to_sync(self.channel_layer.group_add)(chat_id, self.channel_name)
    #     else:
    #         async_to_sync(self.channel_layer.group_send)(chat_id, {'type': 'chat.message', 'message': message})
    #         # return '111111111'

    def websocket_receive(self, message):
        print('2222222222222接收消息', message)
        data = json.loads(message['text'])
        chat_type = data.get('chat_type')
        chat_id = data.get('chat_id')
        chat_content = data.get('message')
        if chat_type == 'add_chat':
            async_to_sync(self.channel_layer.group_add)(chat_id, self.channel_name)
        # 通知组内的所有客户端，执行 xx_oo 方法，在此方法中自己可以去定义任意的功能。
        else:
            async_to_sync(self.channel_layer.group_send)(chat_id, {"type": 'chat.massage', 'message': message})

        # 这个方法对应上面的type，意为向1314组中的所有对象发送信息

    def chat_massage(self, event):
        print('>>>>>>>>>>>33333333333——event', event)
        text = event['message']['text']
        print('>>>>>>>>>>>444444444444444text', text)
        self.send(text)

    def websocket_discard(self, message):
        # 断开链接要将这个对象从 channel_layer 中移除
        print('5555555555555555555', message)
        async_to_sync(self.channel_layer.group_discard)('1', self.channel_name)
        raise StopConsumer()
