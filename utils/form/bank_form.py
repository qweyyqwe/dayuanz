# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : bank_form.py
# @Software: PyCharm


"""
自定义form表单验证
"""
from django import forms


class BankUserForm(forms.Form):
    """
    添加积分商品表单验证
    """
    name = forms.CharField(max_length=100)
    card_id = forms.CharField(max_length=18, min_length=18)
    phone = forms.CharField(max_length=11, min_length=11)
    bank_card_id = forms.CharField(max_length=20)
    password = forms.CharField(max_length=6, min_length=6)
