# Create your views here.

# import 导包
import logging
import random
import re
import string
import time
import traceback
import uuid
import base64
import json
import hmac
import requests
import urllib
import redis

from django.contrib.auth.hashers import check_password
from _sha256 import sha256
from urllib.parse import urlencode
from captcha.image import ImageCaptcha
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.shortcuts import HttpResponse, redirect
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler

from utils.redis_cache import mredis
from utils.resource import get_resource_list, menu_left_list
from utils.token.myjwt import jwt_token
from .models import User, Friends, Resource, Blacklist
from .serializers import UserSer, FriendsSer, ResourceSer, BlacklistSer

logger = logging.getLogger('log')


class Register(APIView):
    """
    # 注册
    """
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['username', 'password', 'password2', 'email', 'phone', 'head', 'signature'],
                                  properties=
                                  {'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
                                   'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
                                   'password2': openapi.Schema(type=openapi.TYPE_STRING, description='确认密码'),
                                   'email': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱'),
                                   'phone': openapi.Schema(type=openapi.TYPE_STRING, description='手机号'),
                                   'head': openapi.Schema(type=openapi.TYPE_STRING, description='头像'),
                                   'signature': openapi.Schema(type=openapi.TYPE_STRING, description='个性签名')}
                                  )

    @swagger_auto_schema(method='post', request_body=request_body)
    @action(methods=['post'], detail=False)
    def post(self, request):
        user_name = request.data.get('username')
        pwd = request.data.get('password')
        re_pwd = request.data.get('password2')
        email = request.data.get('email')
        phone = request.data.get('phone')
        if not all([user_name, pwd, phone]):
            return Response({'msg': '用户信息不全', 'code': 500})
        if pwd != re_pwd:
            return Response({'msg': '两次密码不一致,请检查', 'code': 500})
        # 加密存入 create_user
        pwd_code = make_password(pwd)
        user = User.objects.get_or_create(username=user_name, password=pwd_code, phone=phone, email=email)
        return Response({'msg': '注册成功', 'code': 200})


class LoginAccount(APIView):
    """
    账号密码登录
    """
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['username', 'password'],
                                  properties=
                                  {'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
                                   'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码')}
                                  )

    @swagger_auto_schema(method='post', request_body=request_body)
    @action(methods=['post'], detail=False)
    def post(self, request):
        user_name = request.data.get('username')
        pwd = request.data.get('password')
        if not all([user_name, pwd]):
            return Response({'msg': '用户信息不全', 'code': 500})
        # 登录
        user = User.objects.get(username=user_name)
        # 密码效验check_password(输入，数据库的)
        rest = check_password(pwd, user.password)
        logger.info('LoginAccount—输入的password{}取出的user.password{}'.format(pwd, user.password))
        if rest is False:
            return Response({'msg': '账号和密码错误', 'code': 400})

        # 加密时生成第二部分的字符串

        # payload_dict = jwt_payload_handler(user)
        # # 生成token
        # token = jwt_encode_handler(payload_dict)

        # 生成jwt
        data = {'data': {'id': user.id, 'name': user.username, 'time': int(time.time())}}
        token = jwt_token.encode_token(data)
        return Response({'username': user.username, 'user_id': user.id, 'token': token, 'code': 200})


class LoginPhone(APIView):
    """
    登录————手机号登录
    """

    # permission_classes = [permissions.AllowAny]
    def post(self, request):
        data = request.data
        phone = data.get('phone')
        code = data.get('code')
        redis_cli = redis.Redis(db=2)
        data = redis_cli.get("sms_%s" % phone)
        if data:
            # 取redis中的验证码
            redis_code = data.decode('utf-8')
            logger.info('LoginPhone—输入的code{}取出的redis_code{}'.format(code, redis_code))
            if redis_code == code:
                user = User.objects.get(phone=phone)
                # TODO 登录成功写入token
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return Response(
                    {'msg': 'ok', 'code': '200', 'user_id': user.id, 'username': user.username, 'token': token})
            else:
                return Response({'msg': '验证码错误', 'code': '400 '})
        else:
            return Response({"msg": "验证码以过期", "code": "401"})


# class SmsCode(APIView):
#   """
#   发送手机验证码
#   """
#   def post(self, request):
#     mobile = request.data.get('phone')
#     # 调用方法
#     result = send_message(mobile)
#     if result['statusCode'] == '172001':
#       return Response({'msg': '网络错误', 'code': '400'})
#     elif result['statusCode'] == '160038':
#       return Response({'msg': '验证码过于频繁', 'code': '400'})
#     else:
#       return Response({'msg': '欧克', 'code': '200'})


class SmsCode(APIView):
    """
    发送手机验证码
    """

    def post(self, request):
        phone = request.data.get('phone')
        img_code = request.data.get('img_code')
        uuid = request.data.get('uuid')
        phone_code = request.data.get('phone_code')
        redis_cli = redis.Redis(db=2)
        redis_img_code = redis_cli.get(uuid)
        # 3.对比返回
        logger.info('SmsCode—输入的img_code{}取出的redis_img_code{}'.format(img_code, redis_img_code))
        if img_code.lower() != redis_img_code.decode().lower():
            # 不一样，返回错误信息
            return Response({'msg': '验证码错误', 'code': 400})
        else:
            return Response({'msg': 'ok'})


class ImgCode(APIView):
    """
    图形验证码
    """

    def get(self, request, uuid):
        # 生成随机的字符串，包含数字和字符
        # string.ascii_letters 所有字母字符串
        # string.digits 所有数字字符串
        # random.sample 随机采集指定位数的字符
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        # 使用captcha 把生成的字符串转化成图片
        # 2.生成图片流
        img = ImageCaptcha()
        # 使用img生成图片
        image = img.generate(salt)
        # 3.把生成的图片验证码字符写入redis
        redis_cli = redis.Redis(db=2)  # 生成redis客户端
        # 给图片验证码的字符串设置有效期
        redis_cli.setex(str(uuid), 60 * 5, salt)
        # 4.返回图片流
        return HttpResponse(image, content_type='image/png')


# 校验图片验证码
class CheckImgCode(APIView):
    """
    校验图片验证码
    """

    def get(self, request):
        # 1.获取前端传来的数据：uuid 用户输入的验证码
        img_code_id = request.query_params('img_id')
        img_code = request.query_params('img_code')
        # 2.根据uuid从redis获取图片验证码字符串
        redis_cli = redis.Redis(db=2)
        # 从redis 中获取图片验证字符串
        redis_img_code = redis_cli.get(img_code_id)
        # 3.对比返回
        logger.info('CheckImgCode—输入的code{}取出的redis_code{}'.format(img_code, redis_img_code))
        if img_code.lower() != redis_img_code.decode().lower():
            # 不一样，返回错误信息
            return Response({'msg': '验证码错误', 'code': 400})
        else:
            return Response({'msg': 'ok'})


# from django.core.mail import send_mail
# send_mail('邮件主题',
#           '123456789',
#           'yang_123456202204@163.com',
#           ['3413299451@qq.com'],  # 这里可以同时发给多个收件人
#           fail_silently=False
#           )

from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class EmailSong(APIView):
    """
    发送邮箱
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone = request.query_params.get('phone')
        try:
            email_user = User.objects.get(phone=phone)
            if not email_user:
                return Response({'code': 406, 'msg': '该用户不存在'})
            email = email_user.email
            # email = 'yang_123456202204@163.com'
            if email is None:
                return Response({'code': 406, 'msg': '该用户未注册邮箱，请注册'})
            subject = '测试邮件主题'
            context = {}
            from_email = email  # 邮件发送人
            recipient_list = ['yang_123456202204@163.com']  # 邮件接收人
            # 这里需要提前写好html的页面
            # email_template_name = 'template.html'
            code = uuid.uuid1().hex
            email_template_name = render_to_string('template.html', {'code': code})
            aa = EmailMessage(subject, email_template_name, from_email, recipient_list)
            aa.content_subtype = 'html'
            aa.send()
            mredis.setex_str(code, 3600, email)
            # t = loader.get_template(email_template_name)  # 导入模板
            # html_content = t.render(context)  # 模板参数
            # msg = EmailMultiAlternatives(subject, html_content, from_email, recipient_list)
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()  # 发送邮件
            return Response({'code': 200})
        except:
            error = traceback.format_exc()
            logger.error('EmailSong—error:{}'.format(error))
            return Response({'code': 406, 'msg': error})


class PutPassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        code = request.query_params.get('code')
        code_undo = mredis.str_get(code).decode()
        if code_undo is not None:
            # 跳转到修改密码页面
            # url = 'http://localhost:8080/email_pass?code={}'.format(code_undo.decode())
            url = 'http://127.0.0.1:8080/email_password?code={}'.format(code_undo)
            return redirect(url)
        else:
            return Response({'code': 400, 'message': '验证失败，请重新操作'})


class DingDingCallBack(APIView):
    """
    钉钉三方登录回调
    """

    def post(self, request):
        # 获取code
        code = request.data.get('code')
        t = time.time()
        # 时间戳
        timestamp = str((int(round(t * 1000))))
        appSecret = 'Fcah25vIw-koApCVN0mGonFwT2nSze14cEe6Fre8i269LqMNvrAdku4HRI2Mu9VK'
        # 构造签名
        signature = base64.b64encode(
            hmac.new(appSecret.encode('utf-8'), timestamp.encode('utf-8'), digestmod=sha256).digest())
        # 请求接口，换取钉钉用户名
        payload = {'tmp_auth_code': code}
        headers = {'Content-Type': 'application/json'}
        res = requests.post('https://oapi.dingtalk.com/sns/getuserinfo_bycode?signature=' + urllib.parse.quote(
            signature.decode("utf-8")) + "&timestamp=" + timestamp + "&accessKey=dingoajf8cqgyemqarekhr",
                            data=json.dumps(payload), headers=headers)
        res_json = res.json()
        if res_json['errcode'] != 0:
            return {'message': res_json['errmsg'], 'code': 500, 'data': {'uid': '110'}}
        unid = res_json['user_info']['unionid']
        # 查找用户是否已经添加绑定关系
        user = OauthUser.objects.filter(uid=unid).first()
        if user:
            # 用户已经添加绑定关系
            if user.user:
                # 直接返回主页面
                return Response({'message': 'ok', 'code': 200, 'data': res})
        return Response({'message': 'Not bind account', 'code': 201, 'data': unid})


class BindDingDing(APIView):
    """
    绑定钉钉账号
    """

    def post(self, request):
        unid = request.data.get('unid')
        username = request.data.get('username')
        password = request.data.get('password')
        user = Login.objects.get(username=username)
        # rest = check_password(password, user.password)
        # if not rest:
        #     return Response({'message': '账号密码错误', 'code': 405})
        oauth = OauthUser.objects.filter(uid=unid).first()
        if oauth:
            return Response({'message': '该用户已经绑定，无法重复绑定', 'code': 403})
        dingding = '钉钉'
        users = Login.objects.get(username=username)
        dingding = OauthUser.objects.create(user=users, uid=unid, oauth_type=dingding)
        dingding.save()
        data = [{
            'username': username, 'id': unid
        }]
        return Response({'message': '绑定成功', 'code': 200, 'data': data})


class FindUser(APIView):
    """
    # TODO 搜索用户(分页)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user_info = request.query_params.get('info')
            user_find = User.objects.filter(Q(username__contains=user_info) | Q(phone__contains=user_info)
                                            | Q(email__contains=user_info)).all()
            user_ser = UserSer(user_find, many=True)
            return Response({'code': 200, "user_list": user_ser.data, 'friend_total': user_find.count()})
        except:
            error = traceback.format_exc()
            logger.error('FindUser——error:{}'.format(error))
            return Response({'code': 406, "msg": '找不到此相关用户'})


class AddFriends(APIView):
    """
    添加好友
    判断该好友是否添加过
                  ——是——返回已添加
                  ——否——校验后添加
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user_id = user.id
        friend_id = request.data.get('friend_id')
        try:
            user_friend = Friends.objects.filter(user_id=user_id, friend_id=friend_id).first()
            if user_friend is not None:
                if user_friend.friend_id == int(friend_id):
                    return Response({'code': 406, 'msg': '该好友已添加'})
            else:
                friend_in = User.objects.filter(id=friend_id)
                if not friend_in:
                    return Response({'code': 400, 'msg': '该数据不合法'})
                else:
                    user = Friends.objects.create(user_id=user_id, friend_id=friend_id)
                    return Response({'code': 200, 'msg': '添加成功'})
            return Response({'msg': 400, 'code': '该用户未添加好友'})
        except:
            error = traceback.format_exc()
            logger.error('AddFriends—error:{}'.format(error))
            return Response({'code': 400, 'msg': error})


class ShowUserFriend(APIView):
    """
    对应用户下的好友
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_id = user.id
        friend = Friends.objects.filter(Q(user_id=user_id) & Q(status=0)).all()
        friend_ser = FriendsSer(friend, many=True)
        # print(friend_ser.data)
        # print(friend.remark_name)
        # return Response({'code': 200})
        return Response({'code': 200, 'friend_ser': friend_ser.data})


class PutFriendName(APIView):
    """
    修改——备注好友名
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user_id = user.id
        friend_id = request.data.get('friend_id')
        friend_name = request.data.get('friend_name')
        try:
            Friends.objects.filter(Q(id=friend_id) & Q(user_id=user_id)).update(remark_name=friend_name)
            return Response({"code": 200, "message": "ok"})
        except:
            error = traceback.format_exc()
            logger.error("error", error)
            return Response({"code": 400, "error": error})


class Invite(APIView):
    """
    生成邀请码
    """

    def post(self, request):
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        if user.invite_code is not None:
            return Response({'code': 406, 'msg': '该用户邀请码已存在'})
        code = str(user_id) + str(random.randint(10000, 99999))
        user_invite = User.objects.get(id=user_id)
        user_invite.invite_code = code
        user_invite.save()
        return Response({'code': 200, 'msg': '生成成功'})


# 校验手机号并绑定
class PhoneBang(APIView):
    def post(self, request):
        # data = json.loads(request.body)
        data = request.data
        user_id = int(data['user_id'])
        phone = data["phone"]
        code = data["code"]
        try:
            # 根据手机号获取验证码
            phones = mredis.str_get(str(phone))
            phone_code = phones.decode()
            if not all([phone]):
                return Response({"message": "手机号不能为空", "code": 201})
            if code != phone_code:
                return {"message": "验证码不正确", "code": 201}
            login = User.objects.filter(phone=phone).count
            sql = "update login set phone='%s' where id=%d" % (phone, int(user_id))
            db1.update(sql)
            return Response({"code": 200, "message": "ok"})
        except:
            error = traceback.format_exc()
            logger.error('PhoneBang—error:{}'.format(error))
            return Response({"code": 400, "error": error})


# 解绑手机号
class UpdatePhones(APIView):
    def post(self, request):
        data = request.data
        user_id = int(data['user_id'])
        phone = data["phones"]
        code = data["code"]
        try:
            # 根据手机号获取验证码
            # phones = mredis.str_get(str(phone))
            # phone_code = phones.decode('utf-8')
            # if code != phone_code:
            #     return {"message": "验证码不正确", "code": 201}
            User.objects.filter(id=user_id).update(phone="")
            return Response({"code": 200, "message": "解绑成功"})
        except:
            error = traceback.format_exc()
            logger.error('UpdatePhone—error:{}'.format(error))
            return Response({"code": 400, "error": error})


# 绑定邮箱
class EmailBang(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        user_id = int(data['user_id'])
        try:
            ret = re.match(r"^[a-zA-Z0-9_]{4,20}@(163|126|gmail)\.com", email)
            if ret:
                subject = '绑定账号'  # 邮件名
                message = '恭喜您绑定账号成功'  # 邮件内容
                from_email = '2892694370@qq.com'  # 发送人
                recipient_list = ['l2892694370@163.com']  # 收件人
                msg = EmailMessage(subject, message, from_email, recipient_list)
                msg.send()
                sql = "update login set email='%s' where id=%d" % (email, int(user_id))
                db1.update(sql)
                return Response({"code": 200, "message": "ok"})
            else:
                return Response({"code": 400, 'msg': '邮箱不符合要求'})
        except:
            error = traceback.format_exc()
            logger.error('EmailBang—error:{}'.format(error))
            return Response({"code": 400, "error": error})


# 绑定账号
class AccountBang(APIView):
    def post(self, request):
        data = request.data
        user_id = data['user_id']
        account = data['account']
        try:
            User.objects.filter(id=user_id).update(account=account)
            return Response({"code": 200, "message": "ok"})
        except:
            error = traceback.format_exc()
            logger.error('AccountBang—error:{}'.format(error))
            return Response({"code": 400, "error": error})


class GetUserRolesList(APIView):
    """
    权限
    """
    serializer_class = ResourceSer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        usse_id = user.id
        users = User.objects.get(id=usse_id)
        resource_list = get_resource_list(users)
        menu_list = menu_left_list(resource_list)
        return Response({'code': 200, 'resource_list': menu_list})


class GetUserInfo(APIView):
    """
     个人信息
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        info = User.objects.get(username=user.username)
        # user_ser = UserSer(info, many=True).data
        user_ser_json = {
            'username': info.username,
            'first_name': info.first_name,
            'last_name': info.last_name,
            'date_joined': info.date_joined,
            'phone': info.phone,
            'email': info.email,
            'begin_time': info.begin_time,
            'integral': info.integral,
            'nickname': info.nickname,
            'birth': info.birth,
            'head': info.head,
            'signature': info.signature,
            'gender': info.gender,
        }
        return Response({'code': 200, 'user_info': user_ser_json})


class CompleteUserInfo(APIView):
    """
    完善信息
        nickname        昵称
        head            头像
        signature       个性签名
        birth           出生日期
        gender          性别
    """
    permission_classes = [permissions.IsAuthenticated]

    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['nickname', 'head', 'signature', 'birth', 'gender'],
                                  properties=
                                  {'nickname': openapi.Schema(type=openapi.TYPE_STRING, description='昵称'),
                                   'head': openapi.Schema(type=openapi.TYPE_STRING, description='头像'),
                                   'signature': openapi.Schema(type=openapi.TYPE_STRING, description='签名'),
                                   'birth': openapi.Schema(type=openapi.TYPE_STRING, description='出生日期'),
                                   'gender': openapi.Schema(type=openapi.TYPE_STRING, description='性别')}
                                  )

    @swagger_auto_schema(method='post', request_body=request_body)
    @action(methods=['post'], detail=False)
    def post(self, request):
        data = request.data
        # 获取到用户名
        user = request.user
        test_form = FormUserInfo(data)
        try:
            if test_form.is_valid():
                # 下面就是验证通过啦
                # logger.info('UpdateUserInfo——{}'.format(request.POST['nickname'],
                #                                         request.POST['head'], request.POST['signature'],
                #                                         request.POST['birth'], request.POST['gender']))
                # result_data = test_form
                # logger.info('CompleteUserInfo—result_data:{}'.format(result_data))
                user_name = User.objects.filter(username=user.username).update(**data)
            logger.error('CompleteUserInfo—error:{}'.format(test_form.errors))
            return Response({'code': 200, 'msg': 'ok'})
        except:
            error = traceback.format_exc()
            logger.error('CompleteUserInfo—error:{}'.format(error))
            return Response({'code': 500, 'msg': 'not ok'})


# class UpdateUserInfo(APIView):
#     """
#     修改完善个人信息
#     """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request):
#         data = request.data
#         test_form = UpdateUser(data)
#         if test_form.is_valid():
#             # 下面就是验证通过啦
#             logger.info(
#                 'UpdateUserInfo——{}'.format(request.POST['nickname'], request.POST['head'], request.POST['signature']))
#         logger.error('UpdateUserInfo——error:{}'.format(test_form.errors))
#         return Response({'code': 200, 'msg': 'ok?'})


from utils.form.user_form import FormTestForm, FormUserInfo


class FormTestView(APIView):
    # def get(self, request):
    #     return render(request, 'form_test.html')
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        test_form = FormTestForm(data)
        if test_form.is_valid():
            # 下面就是验证通过啦
            logger.info('UpdateUserInfo——{}'.format(request.POST['name'], request.POST['email']))
        logger.error('FormTestView——{}'.format(test_form.errors))
        return Response({'code': 200, 'msg': 'ok?'})


from .serializers import RoleInfoSerializer


class GetAllRole(generics.GenericAPIView):
    """
    获取所有的角色数据
    """
    serializer_class = RoleInfoSerializer
    # TODO 增加自定义权限
    permission_classes = [permissions.IsAuthenticated]

    query_param = []

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        role_list = Resource.objects.all()
        data = self.get_serializer(role_list, many=True).data
        return Response({'code': 200, 'data': data})


class AllResource(APIView):
    """
    所有资源
    """

    parser_classes = [permissions.IsAuthenticated]

    def get(self, request):
        resource = Resource.objects.all()
        resource_ser = ResourceSer(resource, many=True)
        return Response({"res": resource_ser.data})


class BlackFriend(APIView):
    """
    将好友添加至黑名单
    """

    permission_classes = [permissions.IsAuthenticated]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['friend_id'], properties=
                                  {'friend_id': openapi.Schema(type=openapi.TYPE_STRING, description='好友id')}
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        friend_id = request.data.get('friend_id')
        print(friend_id)
        friend = Friends.objects.get(id=friend_id)
        try:
            friend = Friends.objects.get(id=friend_id)
            print(friend)
            if not friend:
                return Response({'msg': '该用户还不是你的好友, 请添加', 'code': 500})
            if int(friend.status) == 1:
                return Response({"msg": "该好友已在黑名单", "code": 400})
            else:
                friend.status = 1
                friend.save()
                return Response({"code": 200, "msg": "添加黑名单成功"})
        except:
            error = traceback.format_exc()
            logger.error('Black_friend{}'.format(error))
            return Response({"code": 400, "msg": error})


# class GetBlackFriend(APIView):
#     """
#     展示黑名单好友
#     """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request):
#         black_friend = Blacklist.objects.filter(status=1)
#         blacks_friend = BlacklistSer(black_friend, many=True).data
#         return Response({"code": 200, "black_friend": blacks_friend})


class GetBlackFriend(APIView):
    """
    用户对应的黑名单
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_id = user.id
        black = Friends.objects.filter(Q(user_id=user_id) & Q(status=1)).all()
        black_ser = FriendsSer(black, many=True)
        return Response({'code': 200, 'black_ser': black_ser.data})


class FackBlackFriend(APIView):
    """
    移除黑名单
    """
    permission_classes = [permissions.IsAuthenticated]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['friend_id'], properties=
                                  {'friend_name': openapi.Schema(type=openapi.TYPE_STRING, description='好友名字')}
                                  )

    @swagger_auto_schema(method='get', request_body=request_body, )
    @action(methods=['get'], detail=False, )
    def get(self, request):
        friend_id = request.query_params.get('friend_id')
        try:
            black_friend = Blacklist.objects.get(friend_id=friend_id)
            black_friend.delete()
            Friends.objects.filter(friend_id=friend_id).update(friend_status=0)
            return Response({"code": 200, "meg": "ok"})
        except:
            error = traceback.format_exc()
            logger.error("FackBlackFriend".format(error))
            return Response({"code": 402, "msg": error})


