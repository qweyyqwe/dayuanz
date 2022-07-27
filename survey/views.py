from django.shortcuts import render

# Create your views here.


import demjson
import xlrd
import logging
import time
import traceback
import json

from django.db.models import Q
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, generics
from rest_framework import generics, mixins, views

from utils.custom_permissions import IsCheckUser
from utils.form.survey_from import UpdateQuestionAnswerForm
from utils.pinstance import PinstanceList
from utils.redis_cache import mredis
from MQPika.teacher_rabbit_product import PublishClass
from .models import Question, Answer
from .serializers import QuestionSer, Answer, AnswerSer, QuestionnaireSer


logger = logging.getLogger('log')
# 问卷调查    https://blog.51cto.com/u_15549234/5139834


class ShowQuestionAnswer(generics.GenericAPIView):
    """
    展示问题/答案

    """
    parser_classes = [permissions.IsAuthenticated]
    # serializer_class = QuestionSer

    def get(self, request):
        # question = Question.objects.all()
        # question_ser = QuestionSer(question, many=True).data
        # for i in question_ser:
        #     print('1111111111111111>>>>>>>>>', i)
        #     # print(i.count)
        #     # for ii in i:
        #     #     print('111——————————————', ii)
        #     #     count = ii.count
        #
        # answer = Answer.objects.all()
        # answer_ser = AnswerSer(answer, many=True).data
        # for r in answer_ser:
        #     print('22222222222222222>>>>>>>>>', r)
        source = Question.objects.all()
        data = QuestionnaireSer(source, many=True).data
        return Response({'code': 200, 'data': data})


# a = [
#     {
#         'id': 1,
#         'Question':问题,
#         'letter': [A/B/C]
#     }
# ]

    # ajax_post_list = [
    #     {
    #         'id': 2,
    #         'caption': "鲁宁爱不是番禺？？",
    #         'tp': 1,
    #
    #     },
    #     {
    #         'id': None,
    #         'caption': "八级哥肾好不好？",
    #         'tp': 3
    #     },
    #     {
    #         'id': None,
    #         'caption': "鲁宁脸打不打？",
    #         'tp': 2,
    #         "options": [
    #             {'id': 1, 'name': '绿', 'score': 10},
    #             {'id': 2, 'name': '翠绿', 'score': 8},
    #         ]
    #     },
    # ]


class AddQuestionAnswer(generics.GenericAPIView):
    """
    管理员添加调查以选项
    """
    permission_classes = [permissions.IsAuthenticated, IsCheckUser]
    # request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
    #                               required=['title', 'count', 'status', 'question_type', 'answer_type',
    #                                         'answer_content'], properties=
    #                               {
    #                                 'title': openapi.Schema(type=openapi.TYPE_STRING, description='标题'),
    #                                 'count': openapi.Schema(type=openapi.TYPE_STRING, description='题目内容'),
    #                                 'status': openapi.Schema(type=openapi.TYPE_STRING, description='状态存在与否'),
    #                                 'question_type': openapi.Schema(type=openapi.TYPE_STRING, description='状态单选多选问答'),
    #                                 'answer_type': openapi.Schema(type=openapi.TYPE_STRING, description='选项类型'),
    #                                 'answer_content': openapi.Schema(type=openapi.TYPE_STRING, description='选项内容'),
    #                                },
    #                               )
    #
    # @swagger_auto_schema(method='post', request_body=request_body, )
    # @action(methods=['post'], detail=False, )

    def post(self, request):
        # TODO 如果用户输入以什么形式输入 [{"answer_content": "123", "answer_type": "A"},
        #  {"answer_content": "456", "answer_type": "B"},{"answer_content": "789", "answer_type": "C"}]
        user = request.user
        user_id = user.id
        try:
            data = request.data
            logger.info('AddQuestionAnswer——data{}'.format(data.dict()))
            # select = json.loads(request.POST.get('select'))
            select = json.loads(data['select'])
            question = Question.objects.create(user_id=user_id, title='1.1', count=(data['count']), question_type=0)
            for i in select:
                answer = Answer.objects.create(questionid_id=question.id, answer_type=i['answer_type'], answer_content=i['answer_content'])
                question.save()
                answer.save()
            return Response({'code': 200, 'msg': '问卷调查添加成功'})
        except:
            error = traceback.format_exc()
            logger.error('AddQuestionAnswer——error:{}'.format(error))
            return Response({'code': 406, 'msg': False})


class UpdateQuestionAnswer(generics.GenericAPIView):
    """
    修改题目以及选择
    """
    permission_classes = [permissions.IsAuthenticated, IsCheckUser]

    def post(self, request):
        try:
            data = request.data
            question_id = request.data.get('question_id')
            select = json.loads(data['select'])
            question = Question.objects.filter(id=question_id)
            if not question:
                return Response({'code': 500, 'msg': '该数据不存在'})
            data = UpdateQuestionAnswerForm(request.data)
            question_id = Question.objects.get(id=question_id).id
            answer = Answer.objects.filter(questionid_id=question_id)
            if data.is_valid():
                data = data.cleaned_data
                for i in select:
                    # (i['answer_type'], i['answer_content'], i['right_wrong'])
                    answer_ = answer.update(answer_type=i['answer_type'], answer_content=i['answer_content'], right_wrong=i['right_wrong'])
                question.updata(title=data['title'], count=(data['count']), question_type=data['question_type'])
                return Response({'code': 200, 'msg': 'ok'})
            error = data.errors.as_json()
            return Response({'code': 406, 'msg': error})
            # source = Question.objects.filter(id=question_id)
            # data = QuestionnaireSer(source).data
            # print(data)
        except:
            error = traceback.format_exc()
            logger.error('UpdateQuestionAnswer——error:{}'.format(error))
            return Response({'code': 500, 'msg': False})


class DelQuestionAnswer(generics.GenericAPIView):
    """
    删除题目
    """
    permission_classes = [permissions.IsAuthenticated, IsCheckUser]
    query_params = [
        openapi.Parameter(name='question_id', in_=openapi.IN_QUERY, description="需删除问题的id", type=openapi.TYPE_STRING)

    ]

    @swagger_auto_schema(method='get', request_body=query_params, )
    @action(methods=['get'], detail=False, )
    def get(self, request):
        user = request.user
        # TODO 做记录
        question_id = request.query_params.get('question_id')
        question = Question.objects.filter(id=question_id)
        if question:
            return Response({'code': 406, 'msg': '该数据不存在'})
        question.updata(status=1)
        question.save()
        return Response({'code': 200, 'msg': '该数据成功删除'})
