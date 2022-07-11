# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : serializers.py
# @Software: PyCharm


"""
签到序列化器
"""

from rest_framework import serializers
from sign_in.models import Reward, DailySignIn


class RewardSer(serializers.ModelSerializer):
    """
    签到奖励表序列化器
    """
    id = serializers.SerializerMethodField()

    class Meta:
        """
        序列化模型
        """
        model = Reward
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class DailySignInSer(serializers.ModelSerializer):
    """
    用户组序列化器
    """
    id = serializers.SerializerMethodField()

    class Meta:
        """
        序列化模型
        """
        model = DailySignIn
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


