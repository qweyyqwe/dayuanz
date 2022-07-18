# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : utils.py
# @Software: PyCharm

import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from child.models import ChatRecord


# 推送站内信
def push(user_id, message):
    """
    推送消息
    :return:
    """
    channel_layer = get_channel_layer()
    chat_user = 'chat_%s' % user_id
    text = {'type': 'websocket.receive',
            'text': json.dumps(message)}
    async_to_sync(channel_layer.group_send)(
        chat_user,
        {
            'type': 'chat.message',
            'message': text
        }
    )


# 添加聊天记录
def add_chat_record(user_id, friend_id, content, group_id):
    """

    添加聊天记录
    :return:
    """
    obj = ChatRecord.objects.create(user_id=user_id, friend_id=friend_id, content=content, group_id=group_id)
    obj.save()



