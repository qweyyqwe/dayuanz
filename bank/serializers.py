# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers

from .models import BankUser, LoanRecord


class BankUserSer(serializers.ModelSerializer):
    class Meta:
        model = BankUser
        fields = "__all__"


class LoanRecordSer(serializers.ModelSerializer):
    # name = serializers.SerializerMethodField()
    loan_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    late_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = LoanRecord
        fields = "__all__"

    # def get_name(self, obj):
    #     return obj.name


