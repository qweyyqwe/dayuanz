# Create your views here.
import itertools
import logging
import traceback

from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
# Create your views here.
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from child.models import Friends
from utils.utils import push
from .models import SendMail, SendAddFriendMail, MailInfo
from .serializers import SendMailSer

# from .serializers import MailSer
# from utils.site_letter_utils import set_mass_send_site_mail

logger = logging.getLogger('log')


# class GetMail(APIView):
#     """
#         展示用户站内信  按时间排序
#     """
#     query_params = []
#
#     @swagger_auto_schema(method='get', manual_parameters=query_params)
#     @action(methods=['get'], detail=False)
#     def get(self, request):
#         try:
#             user = request.user
#             # 读取并保存群发的站内信
#             set_mass_send_site_mail(user)
#             # 获取用户的站内信
#             mail_total = SiteMail.objects.filter(user=user)
#             # TODO 分页
#             ser = MailSer(mail_total, many=True).data
#             return Response({'msg': '展示', 'code': 200, 'data': ser})
#         except:
#             error = traceback.format_exc()
#             logger.error(error)
#             return Response({'code': 500, 'error': error})


# 注意只有管理员可以添加
# class AddMessageType(APIView):
#     """添加信息类别"""
#     request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
#                                   required=['name', 'content', 'title'],
#                                   properties=
#                                   {'name': openapi.Schema(type=openapi.TYPE_STRING, description='类别名称'),
#                                    'content': openapi.Schema(type=openapi.TYPE_STRING, description='信息内容'),
#                                    'title': openapi.Schema(type=openapi.TYPE_STRING, description='信息标题'),
#                                    }
#                                   )
#
#     @swagger_auto_schema(method='post', request_body=request_body, )
#     @action(methods=['post'], detail=False, )
#     def post(self, request):
#         try:
#             name = request.data.get('name')
#             content = request.data.get('content')
#             title = request.data.get('title')
#             if not all([name, content, title]):
#                 return Response({"msg": '信息类别不全', 'code': 400})
#             if len(name) > 20:
#                 return Response({'msg': '类别长度过长', 'code': 400})
#             if len(content) > 200:
#                 return Response({'msg': '内容信息过长', 'code': 400})
#             if len(title) > 20:
#                 return Response({'msg': '标题过长', 'code': 400})
#             # 全部唯一
#             obj, _ = MessageType.objects.get_or_create(name=name, content=content, title=title)
#             obj.save()
#             return Response({'code': '200', 'msg': '信息类别添加成功'})
#         except:
#             error = traceback.format_exc()
#             logger.error(error)
#             return Response({'code': 500, 'error': error})


# class LookMessageType(APIView):
#     """获取信息类别"""
#     query_param = []
#
#     @swagger_auto_schema(method='get', manual_parameters=query_param)
#     @action(methods=['get'], detail=False)
#     def get(self, request):
#         message_type = MessageType.objects.all()
#         ser = MessageTypeSer(message_type, many=True).data
#         return Response({'msg': "查看类别成功", 'data': ser, 'code': 200})


# class DeleteMessageType(APIView):
#     """删除信息类别"""
#     request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
#                                   required=['id'],
#                                   properties=
#                                   {'id': openapi.Schema(type=openapi.TYPE_STRING, description='类别id'),
#                                    }
#                                   )
#
#     @swagger_auto_schema(method='post', request_body=request_body, )
#     @action(methods=['post'], detail=False, )
#     def post(self, request):
#         try:
#             id = request.data.get('id')
#             message_type = MessageType.objects.filter(id=id).first()
#             if not message_type:
#                 return Response({'msg': "没有该类别或者类别已经被删除", 'code': 200})
#             else:
#                 message_type.delete()
#             return Response({'msg': '类别删除成功', 'code': 200})
#         except:
#             error = traceback.format_exc()
#             logger.error(error)
#             return Response({'code': 500, 'error': error})


# 默认管理员发送
# class AddMail(APIView):
#     """站内消息"""
#     request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
#                                   required=['message_type_id', 'user_id'],
#                                   properties=
#                                   {'message_type_id': openapi.Schema(type=openapi.TYPE_STRING, description='类别id'),
#                                    'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='收到人'),
#                                    }
#                                   )
#
#     @swagger_auto_schema(method='post', request_body=request_body, )
#     @action(methods=['post'], detail=False, )
#     def post(self, request):
#         try:
#             # 类别信息 id
#             message_type_id = request.data.get('message_type_id')
#             # 0是每个都能收到 user_id 是独一无二
#             user_id = request.data.get('user_id')
#             if not all([message_type_id, user_id]):
#                 return Response({"msg": '站内信息不全', 'code': 400})
#             message_type = MessageType.objects.filter(id=message_type_id)
#             if not message_type:
#                 return Response({"msg": "没有该类型信息", 'code': 400})
#             # 群发
#             if int(user_id) == 0:
#                 user = User.objects.filter()
#                 for i in user:
#                     add_mail = Mail.objects.create(message_type_id=message_type.id, user_id=i.id,
#                                                    create_time=timezone.now())
#                     add_mail.save()
#                     return Response({"msg": "全体站内信息添加成功", 'code': 200})
#             add_mail = Mail.objects.create(message_type_id=message_type_id, user_id=user_id)
#             add_mail.save()
#             return Response({"msg": "站内信息添加成功", 'code': 200})
#         except:
#             error = traceback.format_exc()
#             logger.error(error)
#             return Response({'code': 500, 'error': error})


# class PutMail(APIView):
#     """修改站内信"""
#     request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
#                                   required=['mail_id', ],
#                                   properties=
#                                   {'mail_id': openapi.Schema(type=openapi.TYPE_STRING, description='类别id'),
#                                    }
#                                   )
#
#     @swagger_auto_schema(method='post', request_body=request_body, )
#     @action(methods=['post'], detail=False, )
#     def post(self, request):
#         try:
#             mail_id = request.data.get('mail_id')
#             mail = Mail.objects.filter(id=mail_id, status=0).first()
#             if not mail:
#                 return Response({"msg": '该信息已经被读取了', 'code': 400})
#             else:
#                 mail.status = 1
#                 mail.save()
#                 return Response({'msg': '修改成功已读', 'code': 200})
#         except:
#             error = traceback.format_exc()
#             logger.error(error)
#             return Response({'code': 500, 'error': error})/


class AddFriendSendMail(APIView):
    """
    站内信添加好友
    """
    permission_classes = [permissions.IsAdminUser]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['user_id', 'friend_id'],
                                  properties=
                                  {'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='用户id'),
                                   'friend_id': openapi.Schema(type=openapi.TYPE_STRING, description='朋友id'),
                                   }
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        user = request.user
        user_id = user.id
        user_name = user.username
        friend_id = request.data.get('friend_id')
        try:
            content = '用户%s请求添加您为好友' % user_name
            title = '添加好友通知'
            SendAddFriendMail.objects.create(content=content, title=title, friend_id=user_id, user=friend_id)
            return Response({'code': 200, 'msg': '正在等待对方回复'})
        except:
            error = traceback.format_exc()
            logger.error(error)
            return Response({'code': 500, 'msg': error})


class GetAddFriendMail(APIView):
    permission_classes = [permissions.IsAdminUser]
    query_params = []

    @swagger_auto_schema(method='get', manual_parameters=query_params)
    @action(methods=['get'], detail=False)
    def get(self, request):
        try:
            user = request.user
            user_id = user.id
            # 读取并保存群发的站内信
            # 获取用户的站内信
            user_messages = SendAddFriendMail.objects.filter(user=user_id).order_by('-send_time')
            data = SendAddFriendMailSer(user_messages, many=True).data
            return Response({'msg': '展示成功', 'code': 200, 'data': data})
        except:
            error = traceback.format_exc()
            logger.error(error)
            return Response({'code': 500, 'error': error})


class GetOneAddFriendMail(APIView):
    permission_classes = [permissions.IsAdminUser]
    query_params = []

    @swagger_auto_schema(method='get', manual_parameters=query_params)
    @action(methods=['get'], detail=False)
    def get(self, request):
        try:
            user = request.user
            user_id = user.id
            # 读取并保存群发的站内信
            # 获取用户的站内信
            mail_id = request.query_params.get('mail_id')
            user_messages = SendAddFriendMail.objects.filter(user=user_id, id=mail_id).first()
            user_messages.status = 1
            user_messages.save()
            data = SendAddFriendMailSer(user_messages).data
            return Response({'msg': '展示成功', 'code': 200, 'data': data})
        except:
            error = traceback.format_exc()
            logger.error(error)
            return Response({'code': 500, 'error': error})


class PutMail(APIView):
    permission_classes = [permissions.IsAdminUser]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['mail_id', ],
                                  properties=
                                  {'mail_id': openapi.Schema(type=openapi.TYPE_STRING, description='类别id'),
                                   }
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        try:
            mail_id = request.data.get('mail_id')
            mail = SendAddFriendMail.objects.filter(id=mail_id, status=0).first()
            mail.status = 1
            mail.save()
            return Response({'code': 200})
        except:
            error = traceback.format_exc()
            logger.error(error)
            return Response({'code': 500, 'error': error})


class AddFirendSite(APIView):
    """
    双向添加好友
    发送添加好友请求
    0同意    1忽略   2拒绝
    firendid    userid
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        try:
            user = request.user
            user_id = user.id
            friend_id = request.data.get('friend_id')
            start = request.data.get('start')

            # TODO 使用from
            if start == 0:
                # 同意
                friend_id = SendAddFriendMail.objects.get(id=site_mail_id).friend_id
                user_ = Friends.objects.filter(user_id=user_id, friend_id=friend_id)
                users_ = Friends.objects.filter(user_id=friend_id, friend_id=user_id)
                if not user_ and users_:
                    user_info = Friends.objects.create(user_id=user_id, friend_id=friend_id, site_mail=site_mail_id,
                                                       handle_status=0)
                    user_infos = Friends.objects.create(user_id=friend_id, friend_id=user_id,
                                                        site_mail=site_mail_id,
                                                        handle_status=0)
                    user_info.save()
                    user_infos.save()
                    return Response({'code': 200, 'msg': '添加好友成功'})
                else:
                    return Response({'code': 400, 'msg': '无需重复添加'})


            elif start == 1:
                # 忽略
                pass
            elif start == 2:
                # 拒绝
                pass
            else:
                return Response({'code': 500, 'msg': '参数不合法'})
        except:
            error = traceback.format_exc()
            logger.error('AddFirendSite——error:{}'.format(error))
            return Response({'code': 500, 'msg': error})


# 默认管理员发送
from child.models import User


class AddMail(APIView):
    """站内消息"""
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['site_mail_type', 'content', 'title'],
                                  properties=
                                  {

                                      'site_mail_type': openapi.Schema(type=openapi.TYPE_STRING, description='信息人群0群发'
                                                                                                             'else指定用户'),
                                      'content': openapi.Schema(type=openapi.TYPE_STRING, description='内容'),
                                      'title': openapi.Schema(type=openapi.TYPE_STRING, description='标题'),
                                  }
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        try:

            data = request.data
            user = request.user
            user_id = user.id
            # 0是每个都能收到 user_id 是独一无二
            site_mail_type = data.get('site_mail_type')
            content = data.get('content')
            title = data.get('title')
            user = User.objects.filter(id=site_mail_type).first()
            # 群发
            if int(site_mail_type) == 0:
                user = User.objects.filter()
                for i in user:
                    add_mail = SendMail.objects.get_or_create(user=i.id, content=content, title=title,
                                                              site_mail_type=site_mail_type)
                    return Response({"msg": "全体站内信息添加成功", 'code': 200})
            elif not user:
                return Response({'msg': '找不到对应用户', 'code': 406})

            add_mail = SendMail.objects.create(user=user_id, content=content, title=title,
                                                      site_mail_type=site_mail_type)
            push(site_mail_type, SendMailSer(add_mail).data)
            return Response({"msg": "站内信息添加成功", 'code': 200})
        except:
            error = traceback.format_exc()
            logger.error('AddMail——error:{}'.format(error))
            return Response({'code': 500, 'error': error})


class GetMail(APIView):
    """展示用户下的未读&已读按照时间"""
    query_params = []

    @swagger_auto_schema(method='get', manual_parameters=query_params)
    @action(methods=['get'], detail=False)
    def get(self, request):
        try:
            # user = request.user
            # user_id = user.id
            # mail1 = SendMail.objects.filter(user=user_id).order_by('-send_time').all()
            # mail2 = SendMail.objects.filter(user=user_id).order_by('-send_time').all()
            # mail_total = itertools.chain(mail1, mail2)
            email = SendMail.objects.order_by('-send_time').all()
            ser = SendMailSer(email, many=True).data
            return Response({'msg': '展示成功', 'code': 200, 'data': ser})

        except:
            error = traceback.format_exc()
            logger.error(error)
            return Response({'code': 500, 'error': error})


class GetChatRecord(APIView):
    """
    聊天记录
    """
    permission_classes = [permissions.IsAuthenticated]
    query_params = []

    @swagger_auto_schema(method='get', manual_parameters=query_params)
    @action(methods=['get'], detail=False)
    def get(self, request):
        pass


# class GetChatRecord(generics.GenericAPIView):
#     """
#     获取聊天记录
#     """
#
#     serializer_class = FriendListSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     query_param = [
#
#     ]
#
#     @swagger_auto_schema(method='get', manual_parameters=query_param)
#     @action(methods=['get'], detail=False)
#     def get(self, request):
#         user = request.user
#         data = request.query_params
#         group_id = data.get('group_id')
#         start_time = data.get('start_time')
#         end_time = data.get('end_time')
#         data = ChatRecord.objects.filter(group_id=group_id, create_time__gte=start_time,
#                                          create_time_lte=end_time)
#         data = self.get_serializer(data, many=True).data
#         return Response({'code': 200, 'data': data})


