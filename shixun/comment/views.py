# 评论
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action

from comment.models import Comment
from comment.serilizers import CommentSer
from comment.utils import get_comment_list
from dynamic.models import Dynamic

from user.models import User


class AddComment(APIView):
    """
    添加评论
    """
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['user_id', 'dynamic_id','content'], properties=
                                  {'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='评论人'),
                                   'dynamic_id': openapi.Schema(type=openapi.TYPE_STRING, description='评论'),
                                   'content': openapi.Schema(type=openapi.TYPE_STRING, description='评论内容')}
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )

    def post(self, request):
        user_id = request.query_params.get('user_id')
        dynamic_id = request.data.get('dynamic_id')
        content = request.data.get('content')
        if not all([user_id, content, dynamic_id]):
            return Response({'code': 400, 'msg': '数据不全'})
        user = User.objects.get(id=user_id)
        dynamic = Dynamic.objects.get(id=dynamic_id)
        Comment.objects.create(user=user, content=content, dynamic=dynamic)
        return Response({'code': 200, 'msg': '添加成功'})


class GetComment(APIView):
    def get(self, request):
        dynamic_id = request.query_params.get('dynamic_id')
        comment = Comment.objects.filter(dynamic_id=dynamic_id)
        comment_ser = CommentSer(comment, many=True)
        comment_list = get_comment_list(comment_ser.data)
        print('>>>>>>>>>>comment_list', comment_list)
        for i in comment_list:
            print('>>>>>>>>>>len', len(i))
            if len(i) > 7:
                children = i['children']
            else:
                return Response({'data': comment_list, 'code': 200})
        return Response({'data': comment_list, 'code': 200, 'children': children})
