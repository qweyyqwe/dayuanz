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
import logging

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

CONN_LIST = []
logger = logging.getLogger('log')


class ChatConsumer(WebsocketConsumer):
    # # 推送站内信
    # chats = dict()
    #
    # def websocket_connect(self, message):
    #     # 接收这个客户端的连接
    #
    #     self.user_id = self.scope['url_route']['kwargs']['user_id']
    #     print(self.user_id)
    #     data = json.loads(message.get('text', '{}'))
    #     # logger.info('websocket_connect:{}'.format(data))
    #
    #     self.chat_user_id = 'chat_%s' % self.user_id
    #     print('userid>>>>>>>>>>', self.chat_user_id)
    #     async_to_sync(self.channel_layer.group_add)(self.chat_user_id, self.channel_name)
    #     print('66666666666')
    #     self.accept()
    #
    # def websocket_receive(self, message):
    #     # 浏览器基于websocket向后端发送数据，自动触发接收消息。
    #     text = message['text']  # {'type': 'websocket.receive', 'text': '阿斯蒂芬'}
    #     print("接收到消息-->", text)
    #     res = {'result': 'ok'}
    #     for conn in CONN_LIST:
    #         conn.send(json.dumps(res))
    #
    # def disconnect(self, close_code):
    #     # 连接关闭时调用
    #     # 将关闭的连接从群组中移除
    #     print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
    #     async_to_sync(self.channel_layer.group_discard(self.chat_user_id, self.channel_name))
    #     # 将该客户端移除聊天组连接信息
    #     ChatConsumer.chats[self.chat_user_id].remove(self)
    #     self.close()
    #
    # def chat_message(self, event):
    #     print('2222222', event)
    #     # Handles the "chat.message" event when it's sent to us.
    #     text = event['message']['text']
    #     self.send(text)

    def websocket_connect(self, message):
        # 接收这个客户端的连接

        self.user_id = self.scope['url_route']['kwargs']['user_id']
        data = json.loads(message.get('text', '{}'))
        logger.info('websocket_connect:{}'.format(data))

        chat_user_id = 'chat_%s' % self.user_id
        async_to_sync(self.channel_layer.group_add)(chat_user_id, self.channel_name)
        self.accept()

    def websocket_receive(self, message):
        # 通知组内的所有客户端，执行 xx_oo 方法，在此方法中自己可以去定义任意的功能。
        logger.info('websocket_receive:{}'.format(message))
        data = json.loads(message.get('text', '{}'))
        chat_type = data.get('chat_type')
        friend_id = int(data.get('friend_id'))
        user_id = int(data.get('user_id'))
        chat_content = data.get('message')
        chat_id = data.get('chat_id')

        # 判断是否是1v1聊天
        if friend_id and user_id:
            if friend_id > user_id:
                chat_id = '%s_%s' % (user_id, friend_id)
            else:
                chat_id = '%s_%s' % (friend_id, user_id)
        # 创建聊天群组
        if chat_type == 'add_chat':
            async_to_sync(self.channel_layer.group_add)(chat_id, self.channel_name)
        else:
            async_to_sync(self.channel_layer.group_send)(chat_id, {"type": "chat.message", 'message': message})

    def chat_message(self, event):
        logger.info('chat_message:{}'.format(event))
        text = event['message']['text']
        self.send(text)

    def websocket_disconnect(self, message):
        if 'text' in message:
            # 断开链接要将这个对象从 channel_layer 中移除
            data = json.loads(message['text'])
            if data:
                chat_id = data.get('chat_id')
                async_to_sync(self.channel_layer.group_discard)(chat_id, self.channel_name)
                raise StopConsumer()


"""
class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 接收这个客户端的连接

        self.user_id = self.scope['url_route']['kwargs']['user_id']
        data = json.loads(message.get('text', '{}'))
        logger.info('websocket_connect:{}'.format(data))

        chat_user_id = 'chat_%s' % self.user_id
        async_to_sync(self.channel_layer.group_add)(chat_user_id, self.channel_name)
        self.accept()

    def websocket_receive(self, message):
        # 通知组内的所有客户端，执行 xx_oo 方法，在此方法中自己可以去定义任意的功能。
        logger.info('websocket_receive:{}'.format(message))
        data = json.loads(message.get('text', '{}'))
        chat_type = data.get('chat_type')
        friend_id = int(data.get('friend_id'))
        user_id = int(data.get('user_id'))
        chat_content = data.get('message')
        chat_id = data.get('chat_id')

        # 判断是否是1v1聊天
        if friend_id and user_id:
            if friend_id > user_id:
                chat_id = '%s_%s' % (user_id, friend_id)
            else:
                chat_id = '%s_%s' % (friend_id, user_id)
        # 创建聊天群组
        if chat_type == 'add_chat':
            async_to_sync(self.channel_layer.group_add)(chat_id, self.channel_name)
        else:
            async_to_sync(self.channel_layer.group_send)(chat_id, {"type": "chat.message", 'message': message})

    def chat_message(self, event): 
        logger.info('chat_message:{}'.format(event))
        text = event['message']['text']
        self.send(text)

    def websocket_disconnect(self, message):
        if 'text' in message:
            # 断开链接要将这个对象从 channel_layer 中移除
            data = json.loads(message['text'])
            if data:
                chat_id = data.get('chat_id')
                async_to_sync(self.channel_layer.group_discard)(chat_id, self.channel_name)
                raise StopConsumer()
"""

# def websocket_disconnect(self, message):
#     CONN_LIST.remove(self)
#     raise StopConsumer()

# def receive_json(self, message, **kwargs):
#     # 收到信息时调用
#     to_user = message.get('to_user')
#     # 信息发送
#     length = len(ChatConsumer.chats[self.chat_user_id])
#     if length == 2:
#         self.channel_layer.group_send(
#             self.chat_user_id,
#             {
#                 "type": "chat.message",
#                 "message": message.get('message'),
#             },
#         )
#     else:
#         self.channel_layer.group_send(
#             to_user,
#             {
#                 "type": "chat.message",
#                 "event": {'message': message.get('message'), 'group': self.chat_user_id}
#             },
#         )
