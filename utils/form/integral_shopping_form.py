# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : integral_shopping_form.py
# @Software: PyCharm


from django import forms


class FormIntegralShopping(forms.Form):
    # Form表单中字段必须跟前端中的name保持一致

    name = forms.CharField(max_length=30, required=True)
    desc = forms.CharField(max_length=168, required=True)
    image = forms.CharField(widget=forms.Textarea, required=True)
    price = forms.CharField(max_length=168, required=True)
    count = forms.CharField(max_length=10, required=True)
    lock_count = forms.CharField(max_length=10, required=True)
