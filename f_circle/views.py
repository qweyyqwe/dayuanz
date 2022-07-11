from django.shortcuts import render

# Create your views here.


import logging
import random
import time
import traceback
from copy import deepcopy

from django.db.models import Q
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.pinstance import PinstanceList
from utils.qiniu_img import get_qiniu_token
from utils.redis_cache import mredis
from utils.custom_permissions import IsCheckUser
from .models import WeChatMoments, WeChatPicture, WeChatComment

logger = logging.getLogger('log')


class AddCircle(APIView):
    """
    发布朋友圈
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        user_id = user.id
        content = data.get('content')
        circles = WeChatMoments.objects.create(userid_id=user_id, content=content)
        circles.save()
        id = circles.id
        if data['img_list']:
            for i in data['img_list']:
                circle = WeChatPicture.objects.get_or_create(url=i, moment_id_id=id)
        return Response({'msg': '发布成功', 'code': 200})


class GetAllCircle(APIView):
    """
    获取朋友圈
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        user = request.user
        user_id = user.id
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        plaza_all = Plaza.objects.filter(Q(start=0) & Q(check_start=2)).order_by('-id')






    # def get(self, request):
    #
    #     plaza_all = Plaza.objects.filter(Q(start=0) & Q(check_start=2)).order_by('-id')
    #     total_count = plaza_all.count()
    #     page_cursor = PinstanceList()
    #     # 分页
    #     data_list = page_cursor.paginate_queryset(plaza_all, request, view=self)
    #     data_list = PlazaSer(data_list, many=True)
    #     return Response({'code': 200, 'friend_ser': data_list.data, 'total_count': total_count})

