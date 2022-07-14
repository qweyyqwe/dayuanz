from django.shortcuts import render

# Create your views here.


import logging
import random
import time
import traceback
import redis

from copy import deepcopy
from django.db.models import Q
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from decimal import *

from utils.form.bank_form import BankUserForm
from utils.pinstance import PinstanceList
from utils.qiniu_img import get_qiniu_token
from utils.redis_cache import mredis
from utils.phone_charm.phone_charm import send_message
from .models import BankUser, LoanRecord
from .serializers import BankUserSer, LoanRecordSer
from utils.custom_permissions import IsCheckUser
from utils.pinstance import PinstanceList

logger = logging.getLogger('log')


class AddBankUser(APIView):
    """
    用户———开户
    """
    permission_classes = [permissions.IsAuthenticated]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['name', 'card_id', 'phone', 'bank_card_id', 'password'], properties=
                                  {'name': openapi.Schema(type=openapi.TYPE_STRING, description='姓名'),
                                   'card_id': openapi.Schema(type=openapi.TYPE_STRING, description='身份证'),
                                   'phone': openapi.Schema(type=openapi.TYPE_STRING, description='手机号'),
                                   'bank_card_id': openapi.Schema(type=openapi.TYPE_STRING, description='银行卡号'),
                                   'password': openapi.Schema(type=openapi.TYPE_STRING, description='银行密码'),
                                   },

                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        try:
            data = BankUserForm(request.data)
            user = request.user
            user_id = user.id
            if data.is_valid():
                data = data.cleaned_data
                user = BankUser.objects.filter(user=user_id)
                if not user:
                    data.update({'user_id': request.user.id})
                    obj = BankUser.objects.create(**data)
                    obj.save()
                    return Response({'code': 200, 'msg': '开户成功'})
                else:
                    return Response({'msg': '用户已开户', 'code': 406})
            error = data.errors.as_json()
            return Response({'code': 407, 'msg': error})
        except:
            error = traceback.format_exc()
            logger.error('AddBankUser——— error:{}'.format(error))
            return Response({'code': 500, 'msg': error})


class GetBankUserInfo(APIView):
    """
    获取当前用户的开户信息情况
    """
    permission_classes = [permissions.IsAuthenticated]

    query_param = []

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        user = request.user
        user_id = user.id
        try:
            user = BankUser.objects.filter(user=user_id)
            print('>>>>>>>>>>>>', user)
            if not user:
                return Response({'code': 406, 'msg': '未获取到该用户的开户信息'})
            bankuser = BankUser.objects.get(user=user_id)
            bank_ser = BankUserSer(bankuser).data
            return Response({'code': 200, 'msg': bank_ser})
        except:
            error = traceback.format_exc()
            logger.error('GetBankUserInfo——error:{}'.format(error))
            return Response({'code': 500, 'msg': error})


class LoanMoney(APIView):
    """
    开户人员借贷
    """

    permission_classes = [permissions.IsAuthenticated]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['loan_money'], properties=
                                  {
                                      'loan_money': openapi.Schema(type=openapi.TYPE_STRING, description='贷款金额'),
                                      'expect': openapi.Schema(type=openapi.TYPE_STRING, description='分期'),


                                   },
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        user = request.user
        user_id = user.id
        loan_money = request.data.get('loan_money')
        phone = request.data.get('phone')
        code = request.data.get('code')
        bank_password = request.data.get('bank_password')
        bank_user = BankUser.objects.filter(user=user_id)
        if not bank_user:
            return Response({'msg': '该用户未进行开户，请开户后尝试', 'code': 500})
        try:
            get_bank_user = BankUser.objects.get(user=user_id)
            if int(loan_money) > 5000:
                return Response({'msg': '超标了！超标了!!!', 'code': 406})
            if bank_password != get_bank_user.password:
                return Response({'msg': '银行卡的密码不一致，请重试', 'code': 406})
            get_bank_filter = LoanRecord.objects.filter(Q(user_id=get_bank_user.id) & Q(status=0)).count()
            if int(get_bank_filter) > 5:
                return Response({'msg': '请还款后再，再次贷款', 'code': 406})
            # 手机验证码
            # redis_cli = redis.Redis(db=2)
            data = mredis.str_get("sms_%s" % phone)
            # 获取的data b字节 转str
            redis_code = str(data, "utf-8")
            print(redis_code, code)
            if redis_code:
                # 取redis中的验证码
                redis_code = data.decode('utf-8')
                logger.info('LoanMoney—输入的code{}取出的redis_code{}'.format(code, redis_code))
                if redis_code == code:

                    # 数据写入redis进行分配
                    bank_key = 'bank_%s' % user_id
                    code = str(user_id) + str(random.randint(10000, 99999)) + str(int(time.time()))
                    mredis.l_push(bank_key, value=code)
                    loan = LoanRecord.objects.create(loan_money=loan_money, user_id=get_bank_user.id, code=code)
                    loan.save()
                    return Response({'msg': '提交申请，待处理', 'code': 200})
                else:
                    return Response({'msg': '验证码错误', 'code': '400 '})
            else:
                return Response({"msg": "验证码以过期", "code": "401"})
        except:
            error = traceback.format_exc()
            logger.error('LoanMoney———error:{}'.format(error))
            return Response({'code': 500, 'msg': error})


class ShowBankUser(APIView):
    """
    展示用户自己经审核通过的申请
    """
    permission_classes = [permissions.IsAuthenticated]
    query_param = [openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="页数大小", type=openapi.TYPE_NUMBER),
                   openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页码", type=openapi.TYPE_NUMBER)]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        user = request.user
        user_id = user.id
        loan_user = BankUser.objects.get(user_id=user_id)
        bank_user = LoanRecord.objects.filter(Q(status=2) & Q(user_id=loan_user.id)).all()

        bank_money_count = bank_user.count()
        bank_money_ser = PinstanceList()
        # 分页
        data_list = bank_money_ser.paginate_queryset(bank_user, request, view=self)
        bank_money_ser = LoanRecordSer(data_list, many=True).data
        return Response({'data': bank_money_ser, 'count': bank_money_count, 'code': '200'})


class GetBankPhone(APIView):
    """
    借贷时手机验证码发送手机验证码
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        mobile = request.data.get('phone')
        # 调用方法
        result = send_message(mobile)
        if result['statusCode'] == '172001':
            return Response({'msg': '网络错误', 'code': '400'})
        elif result['statusCode'] == '160038':
            return Response({'msg': '验证码过于频繁', 'code': '400'})
        else:
            return Response({'msg': '欧克', 'code': '200'})


class GetAllLoanMoney(APIView):
    """
    审核员 获取自己要处理的数据
    """

    permission_classes = [permissions.IsAuthenticated, IsCheckUser]
    query_param = []

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        data = request.query_params
        page = data.get('page')
        size = data.get('size')
        bank_money_list = LoanRecord.objects.filter(Q(status=0) | Q(status=1) & Q(user_id=request.user.id)).all()
        bank_money_count = bank_money_list.count()
        bank_money_ser = PinstanceList()
        # 分页
        data_list = bank_money_ser.paginate_queryset(bank_money_list, request, view=self)
        bank_money_ser = LoanRecordSer(data_list, many=True).data
        return Response({'data': bank_money_ser, 'count': bank_money_count, 'code': '200'})


class GetNotLoanMoney(APIView):
    """
    获取未分配的借贷请求
    """

    permission_classes = [permissions.IsAdminUser, IsCheckUser]
    query_param = [openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="页数大小", type=openapi.TYPE_NUMBER),
                   openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页码", type=openapi.TYPE_NUMBER)]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        data = request.query_params
        # page = data.get('page')
        # size = data.get('size')
        bank_money_list = LoanRecord.objects.filter(status=0).all()
        bank_money_count = bank_money_list.count()
        bank_money_ser = PinstanceList()
        # 分页
        data_list = bank_money_ser.paginate_queryset(bank_money_list, request, view=self)
        bank_money_ser = LoanRecordSer(data_list, many=True).data
        return Response({'data': bank_money_ser, 'count': bank_money_count, 'code': '200'})


