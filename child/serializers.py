# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : serializers.py
# @Software: PyCharm

from .models import User, Friends, Resource, Blacklist, ChatRecord
from rest_framework import serializers
from django.forms import model_to_dict


class UserSer(serializers.ModelSerializer):
    """
    用户序列化器
    """
    class Meta:
        model = User
        fields = "__all__"


class FriendsSer(serializers.ModelSerializer):
    friend_name = serializers.SerializerMethodField()
    """
    朋友序列化器
    """

    def get_friend_name(self, obj):
        return obj.friend_id.username
    class Meta:
        model = Friends
        fields = "__all__"


class BlacklistSer(serializers.ModelSerializer):
    """
    黑名单序列化器
    """
    class Meta:
        model = Blacklist
        fields = "__all__"


class ResourceSer(serializers.ModelSerializer):
    """
    资源列表序列化器
    """
    class Meta:
        model = Resource
        fields = "__all__"


class RoleInfoSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    tid = serializers.SerializerMethodField()
    class Meta:
        """
        序列化模型
        """
        model = Resource
        fields = ['id', 'name', 'children', 'desc', 'tid']

    def get_tid(self, obj):
        return obj.id

    def get_children(self, obj):
        resource_query_list = obj.resource.all()
        resource_list = []
        for i in resource_query_list:
            if i.status == 1:
                data = model_to_dict(i)
                data.update({'tid': int(str(obj.id) + str(i.id))})
                resource_list.append(data)
        # resource_list = [model_to_dict(i).update({'tid': str(obj.id) + str(i.id)}) for i in resource_query_list if i.status == 1]
        return resource_list


class ChatRecordSer(serializers.ModelSerializer):
    """
    用户组序列化器
    """
    id = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta:
        """
        序列化模型
        """
        model = ChatRecord
        fields = ['message', 'id']

    def get_id(self, obj):
        return obj.id

    def get_message(self, obj):
        text = demjson.decode(obj.content)['text']
        message = demjson.decode(text)
        return message
