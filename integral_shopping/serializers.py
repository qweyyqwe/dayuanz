# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : serializers.py
# @Software: PyCharm


from rest_framework import serializers

from .models import PointsMall, Record


class PointsMallSer(serializers.ModelSerializer):
    class Meta:
        model = PointsMall
        fields = "__all__"


class RecordSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Record
        fields = "__all__"


