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
from utils.images.qiniu_img import get_qiniu_token
from utils.redis_cache import mredis
from .models import Plaza, Discuss
from .serializers import PlazaSer
from utils.custom_permissions import IsCheckUser

logger = logging.getLogger('log')
reviewer_plaza_log = logging.getLogger('check_plaza')


class AddPlaza(APIView):
    """
    发布动态
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        user_id = user.id
        title = data['title']
        content = data['content']
        code = str(1) + str(random.randint(10000, 99999)) + str(int(time.time()))
        try:
            redis_key = 'plaza1'
            plaze_exist = mredis.l_push(redis_key, value=code)
            # etime = time.strftime("%Y-%m-%d %H:%M:%S")
            trends = Plaza.objects.get_or_create(userid=user_id, title=title, content=content, code=code)
            # trends.save()
            return Response({"code": 200, "message": "ok"})
        except:
            error = traceback.format_exc()
            logger.error(error)
            return Response({"code": 406, "message": "发布失败"})


# # 分配审核人
# def set_audit(auditid):
#     count = mredis.t_len('plaza1') TODO 个数大于0则有数据邮箱通知审核员
#     if count > 0:
#         code = mredis.r_pop('plaza1').decode()
#         # 根据code解析userid
#         user_id = code[:-15]
#         number = int(user_id) % 2
#         # 给内容更新审核人
#         sql = "update mes%d set auditid=%d where code='%s'" % (int(number), int(auditid), code)
#         mredis.update(sql)


# @release_bp.route('/auditmes')
# def auditmes():
#     # 获取审核人
#     list_sql = "select id from users where role_id =4"
#     list_sql = [3,4]
#     while True:
#         for i in list_sql:
#             set_audit(i)


class Qiniuyun(APIView):
    """
    获取七牛云token
    """

    def get(self, request):
        return Response({'code': 200, 'token': get_qiniu_token()})


class AllPlaza(APIView):
    """
    展示所有动态
    """

    def get(self, request):
        data = request.query_params
        page = data.get('page')
        size = data.get('size')
        # plaza_all = Plaza.objects.all().order_by('-id')
        # plaza_ser = PlazaSer(plaza_all, many=True)
        plaza_all = Plaza.objects.filter(Q(start=0) & Q(check_start=2)).order_by('-id')
        total_count = plaza_all.count()
        page_cursor = PinstanceList()
        # 分页
        data_list = page_cursor.paginate_queryset(plaza_all, request, view=self)
        data_list = PlazaSer(data_list, many=True)
        return Response({'code': 200, 'friend_ser': data_list.data, 'total_count': total_count})


# class AllPlaza(APIView):
#     """
#     展示所有动态
#     """
#
#     def get(self, request):
#         dynamic_list = Plaza.objects.filter(Q(start=0) & Q(check_start=2))
#         page_cursor = PinstanceList()
#         total_count = dynamic_list.count()
#         data_list = page_cursor.paginate_queryset(dynamic_list, request, view=self)
#         data_list = PlazaSer(data_list, many=True).data
#         return Response({'code': 200, 'data': data_list, 'total_count': total_count})


class AddDiscuss(APIView):
    """
    添加评论
    """

    def post(self, request):
        data = request.data
        user_id = 1  # 用户id
        plaza_id = data.get('plaza_id')  # 动态id
        discuss_fatherid = data.get('discuss_id')  # 被评论id
        content = data.get('content')
        # 判断课程是否存在
        try:
            course = Plaza.objects.get(id=plaza_id)
            if not course:
                return {'message': 'course_id is error', 'code': 200}
            discuss_id = Discuss.objects.get(id=discuss_fatherid)
            if not discuss_id:
                return {'message': 'discuss_id no exist', 'code': 200}
            comment = Discuss.objects.get_or_create(uid=user_id, plazaid=plaza_id, discuss_fatherid=discuss_fatherid,
                                                    content=content, starts=0)
            return Response({'message': 'ok'})
        except:
            error = traceback.format_exc()
            logger.error('AddComment is error:{}'.format(error))
            return Response({'message': error})


class GetDiscuss(APIView):
    """
    获取评论
    """

    def get(self, request):
        plaza_id = request.query_params['plaza_id']
        # comments = Plaza.objects.filter(id=plaza_id).order_by(Plaza.begin_time).all()
        comments = Plaza.objects.filter(id=plaza_id).all()
        # comment_list = mredis.setex_str("11", 60*2, comments)
        result = []
        for comment in comments:
            comment.update({
                'childlist': [],
                'user_info': {
                    'username': '1'
                },
                'is_favorite': 0,
                'count': 10
            })

            childlist = deepcopy(comment)
            childlist = [childlist]
            comment.update({
                'childlist': childlist
            })
            result.append(comment)

        return Response({'msg': result, 'code': 200})


class ReviewerList(APIView):
    """
    审核人——需审核的列表
    """

    def get(self, request):
        user_id = request.query_params.get('user_id')
        plaza_list = Plaza.objects.filter(checkid=user_id)
        data_list = PlazaSer(plaza_list, many=True).data
        return Response({'code': 200, 'data': data_list})


class CheckPlaza(APIView):
    """
    审核
    """
    permission_classes = [permissions.IsAdminUser, IsCheckUser]

    def post(self, request):
        user_id = request.data.get('user_id')
        plaza_id = request.data.get('plaza_id')
        type = request.data.get('type')
        check_content = request.data.get('check_content')
        plaza = Plaza.objects.get(id=plaza_id)
        if plaza.start != 0:
            return Response({'code': 406, 'msg': '该动态已删除'})
        if plaza.check_start == 2:
            return Response({'code': 406, 'msg': '该动态已通过，无需审核'})
        if plaza.check_start == 0:
            if type == 1:
                # 通过状态是2
                reviewer_plaza_log.error('ReviewerPlaza[{}]:{}————{}'.format(plaza_id, plaza.start, user_id))
                return Response({'code': 200, 'msg': '审核通过允许发布'})
            if type == 2:
                # 不通过状态是3
                reviewer_plaza_log.error('ReviewerPlaza[{}]:{}————{}'.format(plaza_id, plaza.start, user_id))
                return Response({'code': 200, 'msg': '该动态不合法，以邮件告知用户'})
        else:
            return Response({'code': 406, 'msg': '参数不合法'})


