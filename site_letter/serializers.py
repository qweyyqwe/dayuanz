# # -*- coding: utf-8 -*-
# # @Time    : 2021/11/22
# # @File    : serializers.py
# # @Software: PyCharm
#
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import MailInfo, SendMail, SendAddFriendMail


class SendMailSer(serializers.ModelSerializer):
    """
    发送站内信息序列化
    """
    send_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SendMail
        fields = "__all__"


class SendAddFriendMailSer(serializers.ModelSerializer):
    """
    发送添加好友站内信息序列化
    """
    send_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SendAddFriendMail
        fields = "__all__"


# class MessageTypeSer(serializers.ModelSerializer):
#     class Meta:
#         model = MessageType
#         fields = '__all__'
#
#
# class MailSer(serializers.ModelSerializer):
#     message_type_name = serializers.SerializerMethodField()
#     message_type_content = serializers.SerializerMethodField()
#     # create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
#
#     def get_message_type_name(self, obj):
#         return obj.content.name
#
#     def get_message_type_content(self, obj):
#         return obj.content.content
#
#     class Meta:
#         model = SiteMail
#         fields = "__all__"

