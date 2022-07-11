from django.shortcuts import render

# Create your views here.

import logging
import traceback

from django.db.models import Q
from django.utils import timezone
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from child.models import User
from utils.form.integral_shopping_form import FormIntegralShopping
from utils.pinstance import PinstanceList
from .models import Reward, DailySignIn
from .serializers import RewardSer, DailySignInSer
logger = logging.getLogger('log')


# class Sign(APIView):
#     """
#     签到
#     规则    签到成功积分加一，
#             连续先到7添加10，后连续天数改0
#             累计签到28天，积分加100， 后累计天数改0
#
#
#     """
#     parser_classes = [permissions.IsAuthenticated]
#
#     def post(self, request, info_data=None):
#         try:
#             user = request.user
#             user_id = user.id
#             # 获取登录的用户是否签到过（未时间一起检测）
#             user_sign_in = DailySignIn.objects.filter(user_id=user_id).count()
#             print('user_sign_in>>>>>>', user_sign_in)
#             # 没签到  则签到
#             if int(user_sign_in) == 0:
#                 user_sign = DailySignIn.objects.create(count=1, target_count=1, user_id=user_id)
#                 sign_in_time = user_sign.create_time.replace(tzinfo=None)
#                 day_time = 86400
#                 sign_in_time_hour = sign_in_time.hour
#                 sign_in_time_minute = sign_in_time.minute
#                 sign_in_time_second = sign_in_time.second
#                 unit_times = sign_in_time_hour * 3600 + sign_in_time_minute * 60 + sign_in_time_second
#                 # 下次签到剩余时间  (距离下次签到还有……)
#                 start_time = day_time - unit_times
#                 user_sign.save()
#                 now_time = timezone.now().replace(tzinfo=None)
#                 times = (now_time - sign_in_time).seconds
#                 if times > start_time:
#                     # 断签了连续签到改0
#                     if times > day_time:
#                         DailySignIn.objects.filter(user_id=user_id).update(count=0)
#                     # 用户积分
#                     integral = User.objects.get(id=user_id).integral  # 积分
#                     count = DailySignIn.objects.get(user_id=user_id).count  # 天数
#                     target_count = DailySignIn.objects.get(user_id=user_id).target_count  # 累计天数
#                     integral += 1
#                     count += 1
#                     target_count += 1
#                     DailySignIn.objects.update(content=count, target_count=target_count, user_id=user_id,
#                                           create_time=now_time)
#                     User.objects.filter(id=user_id).update(integral=integral)
#                     if count == 7:
#                         integral += 10
#                         User.objects.filter(id=user_id).update(integral=integral)
#                     if count == 28:
#                         integral += 100
#                         DailySignIn.objects.filter(user_id=user_id).update(target_count=0, content=0)
#                 # return Response({'code': 200, 'msg': '签到成功', 'start_time': start_time})
#                 return Response({'code': 200, 'msg': '签到{}添加了{}积分'.format(count, integral), 'start_time': start_time})
#             # else:
#             #     print('111111111111111111')
#             #     sign_in_time = DailySignIn.objects.get(user_id=user_id).create_time.replace(tzinfo=None)
#             #     now_time = timezone.now().replace(tzinfo=None)
#             #     times = (now_time - sign_in_time).seconds
#             #     day_time = 86400
#             #     sign_in_time_hour = sign_in_time.hour
#             #     sign_in_time_minute = sign_in_time.minute
#             #     sign_in_time_second = sign_in_time.second
#             #     # 上次签到的时候超过十二点多少秒
#             #     unit_times = sign_in_time_hour * 3600 + sign_in_time_minute * 60 + sign_in_time_second
#             #     start_time = day_time - unit_times
#             #     print('>>>>>>>>>>>>>>>>>time_time', start_time)
#             #     if times > start_time:
#             #         target_count = DailySignIn.objects.get(user_id=user_id).target_count
#             #         content = DailySignIn.objects.get(user_id=user_id).content
#             #         target_count += 1
#             #         content += 1
#             #         user_integral += 1
#             #         DailySignIn.objects.update(content=content, target_count=target_count, user_id=user_id,
#             #                                   create_time=now_time)
#             #         User.objects.filter(id=user_id).update(integral=user_integral)
#             #         if content == 7:
#             #             user_integral += 10
#             #             User.objects.filter(id=user_id).update(integral=user_integral)
#             #         if content == 28:
#             #             user_integral += 100
#             #             User.objects.filter(id=user_id).update(integral=user_integral)
#             #             DailySignIn.objects.filter(user_id=user_id).update(target_count=0, content=0)
#             #     else:
#             #         return Response({'code': 400, 'msg': '无法重复签到'})
#             else:
#                 return Response({'code': '406', 'msg': '您今天已签到'})
#         except:
#             error = traceback.format_exc()
#             logger.error('Sign——error:{}'.format(error))
#             return Response({'code': 406, 'msg': error})


class GetRewardList(APIView):
    """
    获取积分列表
    """
    serializer_class = RewardSer
    permission_classes = [permissions.IsAuthenticated]

    query_param = []

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        data_list = Reward.objects.all()
        result = RewardSer(data_list, many=True).data
        return Response({'code': 200, 'data': result})


class GetUserSignInfo(APIView):
    """
    获取用户签到数据
    防止用户第一次登录没有数据
    """
    serializer_class = DailySignInSer
    permission_classes = [permissions.IsAuthenticated]

    query_param = []

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        user = request.user
        obj, _ = DailySignIn.objects.get_or_create(user=user)
        obj.save()
        result = DailySignInSer(obj).data
        return Response({'code': 200, 'data': result})


# class UserSignInView(APIView):
#     """
#     签到
#     """
#     permission_classes = [permissions.IsAuthenticated]
#
#     request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
#                                   required=[], properties={})
#
#     @swagger_auto_schema(method='post', request_body=request_body, )
#     @action(methods=['post'], detail=False, )
#     def post(self, request):
#         user = request.user
#         integral = user.integral
#         # 获取用户的签到数据对象
#         user_sign = DailySignIn.objects.filter(user=user).first()
#         # 1 判断是否可以签到 当前时间和上次签到时间对比
#         if check_time_is_same_daily(timezone.now(), user_sign.sign_in_time):
#             return Response({'code': 200, 'data': '今天已签到，无法重复签到'})
#         # 判断是否达到一个签到周期
#         # 签到周期从数据库中获取
#         days = Reward.objests.all().last().days
#         # 达到签到周期，重置
#         if user_sign.continuous_day >= days:
#             user_sign.continuous_day = 0
#         # 判断是否连续
#         if check_time_is_continue(timezone.now(), user_sign.sign_in_time):
#             # 连续签到处理
#             user_sign.continuous_day += 1
#         else:
#             # 不连续签到处理
#             user_sign.continuous_day = 0
#             user_sign.continuous_day += 1
#         reward = Reward.objects.filter(days=user_sign.continuous_day).first()
#         # 修改积分
#         user.add_invite_integral(reward.reward_coin, '签到积分')
#         # 记录签到时间
#         user_sign.sign_in_time = timezone.now()
#         user_sign.save()
#         return Response({'code': 200, 'msg': '恭喜签到成功'})


class SignServer(APIView):
    """
    签到2， 连续7天积分加5，  后连续天数在下一次改  0+1
    """
    permission_classes = [permissions.IsAuthenticated]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=[],
                                  properties={})

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        try:
            user = request.user
            user_id = user.id
            print(user_id)
            user_sign = DailySignIn.objects.filter(user=user)
            user_sign2 = DailySignIn.objects.get(user=user)
            user_sign3 = User.objects.get(id=user_id)
            print(user_sign2.continuous_day)
            print(user_sign3.integral)
            print('————————————————')
            if not user_sign:
                sign = DailySignIn.objects.create(continuous_day=1, user=user, sign_in_time=timezone.now())
                return Response({'code': '200', 'msg': '签到成功'})
            else:
                # 现在时间
                now_time_day = timezone.now().replace(tzinfo=None).day
                # now_time_day = "2022-07-02 10:42:48.467544"
                # 获取上次签到时间与现在时间比较  日
                sign_day = user_sign2.sign_in_time.day
                if now_time_day == sign_day:
                    return Response({'code': 400, 'msg': '今天已签到'})
                elif now_time_day < sign_day:
                    return Response({'code': 400, 'msg': '发送意外时间，稍后重试'})
                else:
                    # 下一次签到
                    integral = User.objects.get(id=user_id).integral  # 积分
                    count = DailySignIn.objects.filter(user=user).count()  # 天数
                    print('count>>>>>>>>>>>>>>>>>', count)
                    integral += 1
                    count += 1
                    DailySignIn.objects.update(continuous_day=count, user=user, sign_in_time=timezone.now())
                    print('修改后的>>>>>>>>>>>>>>>>>>>>', user_sign2.continuous_day)
                    print('修改后的>>>>>>>>>>>>>>>>>>>>', user.integral)
                    User.objects.filter(id=user_id).update(integral=integral)
                    # 连续7天签到
                    if count == 7:
                        integral += 10
                        User.objects.filter(id=user_id).update(integral=integral)
                        DailySignIn.objects.filter(user=user).update(continuous_day=0)
                return Response({'code': 200, 'msg': '签到成功', 'day_count': user_sign2.continuous_day})
                # return Response({'code': 406, 'msg': '????????'})
        except:
            error = traceback.format_exc()
            logger.error('SignServer——error:{}'.format(error))
            return Response({'code': 500, 'msg': error})
