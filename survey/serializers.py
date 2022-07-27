# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers

from .models import Question, Answer


class QuestionSer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class AnswerSer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class QuestionnaireSer(serializers.ModelSerializer):
    select = serializers.SerializerMethodField()

    def get_select(self, obj):
        select = Answer.objects.filter(questionid=obj.id)
        data = {}
        for i in select:
            data[i.answer_type] = i.answer_content
        return data

    class Meta:
        model = Question
        fields = "__all__"
