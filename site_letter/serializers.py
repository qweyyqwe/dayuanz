# # -*- coding: utf-8 -*-
# # @Time    : 2021/11/22
# # @File    : serializers.py
# # @Software: PyCharm
#
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import SendMail, SendAddFriendMail


class SendAddFriendMailSer(serializers.ModelSerializer):
    """
    发送添加好友站内信息序列化
    """
    send_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SendAddFriendMail
        fields = "__all__"


class SendMailSer(serializers.ModelSerializer):
    class Meta:
        model = SendMail
        fields = "__all__"

