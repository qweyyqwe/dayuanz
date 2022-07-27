# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : survey_from.py
# @Software: PyCharm

from django import forms


class AddQuestionAnswerForm(forms.Form):
    """
    管理员添加问卷的题目以选项
    """
    title = forms.CharField(max_length=68, required=True)
    count = forms.Textarea()
    status = forms.IntegerField(max_value=1, min_value=0, required=True)
    question_type = forms.IntegerField(max_value=3, min_value=0, required=True)


class UpdateQuestionAnswerForm(forms.Form):
    """
    修改内容
    """
    title = forms.CharField(max_length=68, required=True)
    count = forms.CharField(max_length=268, required=True)
    # count = forms.Textarea()
    status = forms.IntegerField(max_value=1, min_value=0, required=True)
    question_type = forms.IntegerField(max_value=3, min_value=0, required=True)
    # right_wrong = forms.BooleanField()
    # answer_type = forms.CharField(max_length=10, min_length=1)
    # answer_content = forms.CharField(max_length=168, min_length=1, required=True)
