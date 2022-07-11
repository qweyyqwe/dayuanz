# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : user_form.py
# @Software: PyCharm


from django import forms


class UpdateUser(forms.Form):
    nickname = forms.CharField(max_length=30, required=True)
    head = forms.CharField(max_length=255, required=True)
    signature = forms.CharField(widget=forms.Textarea)
    if nickname is False:
        raise forms.ValidationError("昵称过长")
    if head is False:
        raise forms.ValidationError("头像过长")


class FormUserInfo(forms.Form):
    # Form表单中字段必须跟前端中的name保持一致

    # def user_info(self, user_id):
    nickname = forms.CharField(max_length=30, required=True)
    head = forms.CharField(max_length=168, required=True)
    signature = forms.CharField(widget=forms.Textarea, required=True)
    birth = forms.CharField(max_length=168, required=True)
    gender = forms.IntegerField(required=True)


class FormTestForm(forms.Form):
    name = forms.CharField(max_length=5, required=True)
    email = forms.EmailField(required=True)



