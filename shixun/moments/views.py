import time

from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action
import logging
from rest_framework.views import APIView

from comment.utils import get_comment_list
from moments.models import PypMoments, PypPicture, PypComment
from moments.serializers import PypMomentsSer, PyqPictureSer, PypCommentSer
from shixun.pagenation import MyPagination
from user.models import User, UserInfo

# 普通log
logger = logging.getLogger('log')


class AddPyp(APIView):
    permission_classes = [permissions.IsAuthenticated]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['content', 'picture_list'], properties=
                                  {'content': openapi.Schema(type=openapi.TYPE_STRING, description='朋友圈内容'),
                                   'picture_list': openapi.Schema(type=openapi.TYPE_STRING, description='朋友圈')}
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        data = request.data
        # print(">>>>>>>>>>>>>>>>data", data)
        user = request.user
        user_id = user.id
        # user_id = request.query_params.get("user_id")
        content = request.data.get('content')
        create_time = time.strftime("%Y-%m-%d %H:%M:%S")
        pyq = PypMoments.objects.create(user_id=user_id, content=content)
        pyq.save()
        id = pyq.id
        print('>>>>>>>>>id', id)
        print('>>>>>>>>>>>>data', data['picture_list'], type(data['picture_list']))
        for i in data['picture_list']:
            i = i
            print('>>>>>>>>>i', i)
            pyq_picture = PypPicture.objects.create(url=i, moments_id=id, create_time=create_time)
            pyq_picture.save()
        return Response({"code": 200, "message": "ok"})


#   获取朋友圈
class GetSelf(GenericAPIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")
        user = PypMoments.objects.filter(user=user_id).order_by("-create_time")
        #   实例化分页对象
        page_cursor = MyPagination()
        #   分页
        data_list = page_cursor.paginate_queryset(user, request, view=self)
        ser = PypMomentsSer(data_list, many=True)
        pyqpicture = PypPicture.objects.filter(moments=user_id)
        pyqpictureser = PyqPictureSer(pyqpicture, many=True).data
        return Response({"msg": ser.data, "code": 200, "pyqpictureser": pyqpictureser})


class GetAll(GenericAPIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")
        friend_list = UserInfo.objects.filter(user_id=user_id).values_list('friend_id', flat=True)
        logger.info('friend_list:{}'.format(friend_list))
        moments = PypMoments.objects.filter(user_id__in=friend_list).order_by("-create_time")
        #   实例化分页对象
        page_cursor = MyPagination()
        #   分页
        data_list = page_cursor.paginate_queryset(moments, request, view=self)
        pyqpictureser = PyqPictureSer(data_list, many=True).data
        return Response({"msg": 'success', "code": 200, "pyqpictureser": pyqpictureser})


class GetAllPyq(APIView):
    def post(self, request):
        pyq = PypMoments.objects.all()
        pyqser = PypMomentsSer(pyq, many=True).data
        pyqpicture = PypPicture.objects.all()
        pyqpictureser = PyqPictureSer(pyqpicture, many=True).data
        logger.info('获取所有好友的朋友圈:{}'.format(pyqpictureser))
        return Response({"code": 200, "message": "ok", "pyqser": pyqser, "pyqpictureser": pyqpictureser})


class AddComment(APIView):
    """添加父评论"""
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['user_id', 'moments_id'], properties=
                                  {'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='用户id'),
                                   'moments_id': openapi.Schema(type=openapi.TYPE_STRING, description='朋友圈id'),
                                   'content': openapi.Schema(type=openapi.TYPE_STRING, description='评论内容'),
                                   'pid': openapi.Schema(type=openapi.TYPE_STRING, description='评论楼中楼'), }
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        user_id = request.data.get('user_id')
        moments_id = request.data.get('moments_id')
        content = request.data.get('content')
        if not all(['user_id', 'moments_id', 'content']):
            return Response({'msg': '该评论的信息不存在', 'code': 400})
        pyp_comment = PypComment.objects.create(user_id=user_id, moments_id=moments_id, content=content)
        pyp_comment.save()
        logger.info('添加朋友圈评论:{}'.format(pyp_comment))
        return Response({'msg': "评论朋友圈成功", 'code': 200})


class AddFloorComment(APIView):
    """添加子评论"""
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['user_id', 'pyp_moments_id'], properties=
                                  {'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='用户id'),
                                   'moments_id': openapi.Schema(type=openapi.TYPE_STRING, description='朋友圈id'),
                                   'content': openapi.Schema(type=openapi.TYPE_STRING, description='评论内容'),
                                   'pid': openapi.Schema(type=openapi.TYPE_STRING, description='评论楼中楼'), }
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        user_id = request.data.get('user_id')
        moments_id = request.data.get('moments_id')
        content = request.data.get('content')
        pid = request.data.get('pid')
        if not all(['user_id', 'pyp_moments_id', 'content', 'pid']):
            return Response({'msg': '该评论的信息不存在', 'code': 400})
        if pid == 0:
            return Response({'msg': '该评论不能为父评论'})
        # 此评论是子评论
        pid_count = PypComment.objects.filter(id=pid).count()
        if pid_count == 0:
            return Response({'msg': '该评论的父类id不存在', 'code': 400})
        pyp_comment = PypComment.objects.create(user_id=user_id, moments_id=moments_id, content=content,
                                                pid=pid)
        pyp_comment.save()
        logger.info('添加朋友圈评论的楼中楼:{}'.format(pyp_comment))
        return Response({'msg': '评论楼中楼添加成功', 'code': 200})


class LookFloorComment(APIView):
    """查看评论"""

    def get(self, request):
        moments_id = request.query_params.get('moments_id')
        logger.info('查看朋友圈的id:{}'.format(moments_id))
        floor_comment = PypComment.objects.filter(moments_id=moments_id)
        ser = PypCommentSer(floor_comment, many=True).data
        logger.info('查看朋友圈评论的数据:{}'.format(ser))
        result = get_comment_list(ser)
        return Response({'code': 200, 'data': result})
