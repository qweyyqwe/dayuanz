import base64
import logging
import datetime
import hmac
import random
import string
import time
import urllib
from hashlib import sha256
import requests
import json
import redis
import traceback
import uuid
from django.shortcuts import redirect
from django.db.models import Q
from urllib.parse import urlencode
from django.contrib.auth.hashers import check_password, make_password
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions, generics
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
import redis
import random
from django.core import mail
from django.core.mail import EmailMessage
from celery_task.tasks import send_message, send_email1
from comment.utils import get_comment_list
from dynamic.views import get_qiniu_token
from shixun.pagenation import MyPagination
from user.models import User, OauthUser, UserInfo, UserInformation, UserGroup, Resource
from rest_framework.response import Response

from user.serializers import UserInfoSerializer, UserSer, UserInformationSerializer, ResourceSer, \
    UserGroupInfoSerializer, UserUserGroupListSer, UserResourceSerializer
from user.utils import UserForm

logger = logging.getLogger('log')

add_log = logging.getLogger('my_logger')


# 生成订单号
def create_invitation_code(order_id):
    invitation_code = str(
        datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(order_id) + str(random.randint(1000, 9999)))
    return invitation_code


class RegisterView(APIView):
    """
    注册
    账号 密码 手机号 验证码
    """

    def post(self, request):
        user_name = request.data.get('username')
        pwd = request.data.get('password')
        phone = request.data.get('phone')
        code = request.data.get('code')
        logging.info('code', code, type(code))
        client = redis.Redis()
        sms_codes = client.get('sms_%s' % phone).decode()
        print('>>>>>>>>>>>>>>>', sms_codes)
        if sms_codes != code:
            return Response({"msg": "验证码错误", 'code': 400})
        if not all([user_name, pwd, phone]):
            return Response({'msg': '用户信息不全', 'code': 500})
        # 判断姓名
        user_name_num = User.objects.filter(username=user_name).count()
        if user_name_num != 0:
            return Response({'msg': '该用户用户名已经注册过', 'code': 500})
        # 判断电话
        phone_num = User.objects.filter(phone=phone).count()
        if phone_num != 0:
            return Response({'msg': '该用户的手机号已经注册', 'code': 500})
        # 加密存入 create_user
        user = User.objects.create_user(username=user_name, password=pwd, phone=phone)
        print('>>>', user)
        return Response({'msg': '注册成功', 'code': 200})


class LoginCommonViews(APIView):
    """
    登录
    账号或密码
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        pwd = request.data.get('password')
        if not all([username, pwd]):
            return Response({'msg': '账号或密码不全', 'code': 400})
        res = User.objects.filter(username=username).count()
        if res == 0:
            return Response({'msg': '账号不存在', 'code': 400})
        else:
            # 登录
            user = User.objects.get(username=username)
            # 密码效验check_password(输入，数据库的)
            rest = check_password(pwd, user.password)
            if not rest:
                return Response({'msg': '账号和密码错误', 'code': 400})
        # token = jwt_token.encode_token({"username": username})
        print('222222', user.id)
        return Response({'msg': 'login success', 'code': 200, 'username': username, 'user_id': user.id})


class LoginPhoneView(APIView):
    """
    手机号验证码登录
    """

    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get('code')
        print(code)
        # 校验短信验证码
        client = redis.Redis()
        msmcodes = client.get('sms_%s' % phone).decode()
        print('>>>>>>>>>>>>>>>', msmcodes)
        # 校验验证码是否过期
        if not msmcodes:
            return Response({'msg': '验证码过期请重新登陆', "code": '204'})
        # 校验验证码是否正确
        if msmcodes != code:
            return Response({'msg': '验证码错误请重新输入', "code": '401'})
        # token = jwt_token.encode_token({"phone": phone})
        return Response({'msg': 'login success', "code": '200'})


# 异步发送
class SendSMSCode(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        print('>>>>>>>>>>>>>>>',phone)
        # 发送短信验证码
        # delay触发异步任务
        resp, sms_code = send_message(phone)
        resp_data = json.loads(resp)
        print(resp_data.get('statusCode'))
        if resp_data['statusCode'] in ["000000", "112310"]:
            # 1.发送成功的验证码写入redis
            # 2.TODO 使用哪一种数据类型：zset，set，hash，list，string
            # 3.用string最简单 string:k:phone v sms_code
            client = redis.Redis()
            # 设置有效期
            client.setex('sms_%s' % phone, 120, sms_code)
            return Response({'msg': '发送短信验证码成功', 'code': '200'})
        else:
            return Response({'msg': '发送短信验证码失败'})


# 通过email找回密码
class GetEmail(APIView):
    def post(self, request):
        # 获取邮箱
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if user:
                code = uuid.uuid1().hex
                print('>>>>>>>>>>>>>>>>>>>code', code)
                try:
                    subject = '重置密码'
                    # context = {}
                    message = "点击'http://localhost:8000/user/pass_code?code={}'进行密码重置".format(code)
                    from_email = '2457304066@qq.com'
                    to_email = ['2457304066@qq.com']
                    # 这里需要提前写好html的页面
                    # email_template_name = 'email.html'
                    # t = loader.get_template(email_template_name)  # 导入模板
                    # html_content = t.render(context)  # 模板参数
                    # msg = EmailMultiAlternatives(subject, html_content, from_email, to_email)
                    # msg.attach_alternative(html_content, "text/html")
                    # msg.send()
                    send_email1.delay(subject, message, from_email, to_email)
                    # 成功存入redis,code为key,邮箱为value加过期时间
                    res = redis.Redis()
                    res.setex(code, 3600, email)
                    res.close()
                    return Response({'code': 200, 'data': code})
                except:
                    error = traceback.format_exc()
                    print('error', error)
                    return Response({'code': 10011, 'message': '发送邮件失败'})
        except:
            # 返回结果
            return Response({'code': 10010, 'message': '邮箱不存在无法进行验证'})


class PassCode(APIView):
    def get(self, request):
        # 获取唯一标识
        code = request.query_params.get('code')
        # 验证
        res = redis.Redis()
        email = res.get(code)
        if email:
            # 跳转到修改密码页面
            url = 'http://localhost:8080/confirmpwd?code={}'.format(code)
            # return redirect(url)
            return Response({'msg': "成功", 'code': '200', "data": url})
        else:
            # 跳转到vue页面提示验证失败，不能进行修改
            pass


class PutPass(APIView):
    def post(self, request):
        try:
            code = request.data.get('code')
            print('>>>>>>>>>>>>>code', code)
            res = redis.Redis()
            email = res.get(code).decode()
            print('>>>>>>>>>>>email', email)
            pwd = request.data.get('password')
            print('>>>>>>>password', pwd)
            password = make_password(pwd)
            user = User.objects.filter(email=email)
            print('>>>>>>>>>>>>user', user)
            user.update(password=password)
            return Response({'code': 200, 'msg': '修改密码成功'})
        except:
            error = traceback.format_exc()
            print('error>>>>>>>>>>', error)


# 手机号找回密码
class GetPhone(APIView):
    """
    手机号验证码修改密码
    """

    def post(self, request):
        phone = request.data.get("phone")
        print('>>>>>>>>>>>>phone', phone)
        code = request.data.get('code')
        print('>>>>>>>>>>>>code', code)
        # 校验短信验证码
        client = redis.Redis()
        msmcodes = client.get('sms_%s' % phone).decode()
        print('>>>>>>>>>>>>>>>', msmcodes)
        # 校验验证码是否过期
        if not msmcodes:
            return Response({'msg': '验证码过期请重新登陆', "code": '204'})
        # 校验验证码是否正确
        if msmcodes != code:
            return Response({'msg': '验证码错误请重新输入', "code": '401'})
        # token = jwt_token.encode_token({"phone": phone})
        return Response({'code': 200, 'msg': '校验成功'})


class PutPhonePass(APIView):
    def post(self, request):
        phone_code = request.data.get('phone_code')
        res = redis.Redis()
        phone = res.get(phone_code).decode()
        pwd = request.data.get('password')
        password = make_password(pwd)
        user = User.objects.filter(phone=phone)
        user.update(password=password)
        return Response({'code': 200, 'msg': '修改密码成功'})


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
        user = User.objects.get(username=username)
        rest = check_password(password, user.password)
        if not rest:
            return Response({'message': '账号密码错误', 'code': 405})
        oauth = OauthUser.objects.filter(uid=unid).first()
        if oauth:
            return Response({'message': '该用户已经绑定，无法重复绑定', 'code': 403})
        dingding = '钉钉'
        users = User.objects.get(username=username)
        dingding = OauthUser.objects.create(user=users, uid=unid, oauth_type=dingding)
        dingding.save()
        data = [{
            'username': username, 'id': unid
        }]
        return Response({'message': '绑定成功', 'code': 200, 'data': data})


# class InvitationCodeView(APIView):
#     def post(self, request):
#         user = request.user
#         user_id = user.id
#         print('>>>>>>>.user_id', user_id)
#         invitation_code = create_invitation_code(user_id)
#         client = redis.Redis()
#         # 设置有效期
#         client.setex('code_{}'.format(invitation_code), 1200, invitation_code)
#         invitation_code_ = client.get('code_%s' % invitation_code).decode()
#         print('>>>>>>>>>>>>>>>', invitation_code_)
#         return Response({'code': 200, 'msg': 'Invitation code generated successfully', 'data': invitation_code_})
#
#
# class InvitationView(APIView):
#     def post(self, request):
#         invitation_code = request.data.get('invitation_code')
#         client = redis.Redis()
#         invitation_code_ = client.get('code_%s' % invitation_code).decode()
#         print('>>>>>>>>>>>>>>>', invitation_code_)
#         # 校验验证码是否过期
#         if not invitation_code_:
#             return Response({'msg': 'Invitation code not saved', "code": '400'})
#         # 校验验证码是否正确
#         if invitation_code_ != invitation_code:
#             return Response({'msg': 'Invitation code input error', "code": '401'})
#         return Response({'code': 200, 'msg': '5000w元宝已到账,隐藏地图已开启'})


class InvitationCodeView(APIView):
    def post(self, request):
        # user = request.user
        # user_id = user.id
        user_id = request.data.get('user_id')
        print('>>>>>>>.user_id', user_id)
        user = User.objects.get(id=user_id)
        if user:
            code = uuid.uuid1().hex
            print('>>>>>>>>>>>>>>>>>>>code', code)
            user_code = User.objects.get(id=user_id).code
            user_count = User.objects.filter(code=user_code).count()
            print('>>>>>>>user_count', user_count)
            if user_count > 0:
                return Response({'code': 400, 'msg': '邀请码已经存在，无需再重复生成'})
            else:
                User.objects.create(code=user_code)
                message = "http://localhost:8000/user/code/?code={}".format(code)
                return Response({'code': 200, 'data': code, 'msg': message})


class CodeViews(APIView):
    def get(self, request):
        # 获取唯一标识
        code = request.query_params.get('code')
        print('>>>>>>>>.code', code)
        # 验证
        user = User.objects.get(code=code)
        print('>>>>>>>>>.user', user)
        if user:
            # 跳转到修改密码页面
            url = 'http://localhost:8080/code_login/?code={}'.format(code)
            return redirect(url)
        else:
            # 跳转到vue页面提示验证失败，不能进行修改
            pass


class CodeLogin(APIView):
    def post(self, request):
        code = request.data.get('code')
        print('>>>>>>>>>>>>>code', code)
        user_name = request.data.get('username')
        pwd = request.data.get('password')
        phone = request.data.get('phone')
        smscode = request.data.get('smscode')
        print('》》》》》》》》》》smscode', smscode, type(smscode))
        client = redis.Redis()
        sms_codes = client.get('sms_%s' % phone).decode()
        print('>>>>>>>>>>>>>>>', sms_codes)
        # 验证
        user = User.objects.get(code=code)
        print('>>>>>>>>>.user', user)
        user_codes = User.objects.filter(code=code).first()
        if not user_codes:
            return Response({'msg': '邀请码错误', 'code': 400})
        if user:
            if sms_codes != smscode:
                return Response({"msg": "验证码错误", 'code': 400})
            if not all([user_name, pwd, phone]):
                return Response({'msg': '用户信息不全', 'code': 500})
            # 判断姓名
            user_name_num = User.objects.filter(username=user_name).count()
            if user_name_num != 0:
                return Response({'msg': '该用户用户名已经注册过', 'code': 500})
            # 判断电话
            phone_num = User.objects.filter(phone=phone).count()
            if phone_num != 0:
                return Response({'msg': '该用户的手机号已经注册', 'code': 500})
            # 加密存入 create_user
            user = User.objects.create_user(username=user_name, password=pwd, phone=phone)
            print('>>>', user)
            if code:
                code_user = User.objects.get(code=code)
                code_user.integral += 10
                code_user.save()
                User.objects.create(username=user_name, password=pwd, phone=phone, integral=10)
                return Response({'msg': '注册成功', 'code': 200})
        else:
            return Response({'msg': '邀请码失效', 'code': 400})


class AddFriend(APIView):
    """
    添加好友
    """
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
        user_id = request.query_params.get('user_id')
        print('>>>>>>>.user_id', user_id)
        friend_id = request.data.get('friend_id')
        try:
            friend = UserInfo.objects.filter(id=friend_id).first()
            friend_ = UserInfo.objects.filter(friend_id=friend_id).first()
            if friend_:
                return Response({'msg': 'No need to add repeatedly', 'code': 401})
            else:
                if not friend:
                    return Response({'code': 400, 'msg': 'No such person found'})
                obj, _ = UserInfo.objects.get_or_create(user_id=user_id, friend_id=friend_id)
                obj.save()
                return Response({'code': 200, 'msg': 'Add friend succeeded'})
        except:
            error = traceback.format_exc()
            return Response({'code': 500, 'msg': error})


class DeleteFriend(APIView):
    """
    删除好友
    """
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
        user_id = request.query_params.get('user_id')
        friend_id = request.data.get('friend_id')
        try:
            users = UserInfo.objects.filter(user_id=user_id, friend_id=friend_id).first()

            if users:
                users.delete()
                return Response({'msg': '删除成功', 'code': 200})
            else:
                return Response({'msg': '好友不存在', 'code': 400})
        except:
            error = traceback.format_exc()
            return Response({'code': 500, 'msg': error})


class SearchFriend(APIView):
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['keyword'],
                                  properties=
                                  {'keyword': openapi.Schema(type=openapi.TYPE_STRING, description='搜索'),
                                   }
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        keyword = request.data.get('keyword')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', keyword)
        # 能搜索
        if keyword:
            friend = UserInfo.objects.filter(
                Q(nick_name__contains=keyword) | Q(friend_id__contains=keyword) | Q(user_id__contains=keyword))
            result = UserInfoSerializer(friend, many=True).data
            return Response({'code': 200, 'data': result, 'msg': '查找成功'})


class GetFriend(ListAPIView):
    """查看好友
    """

    def post(self, request):
        user_id = request.data.get('user_id')
        print('>>>>>>>>>>>user_id', user_id)
        friend = UserInfo.objects.filter(user_id=user_id)
        data = UserInfoSerializer(friend, many=True).data
        return Response({"code": 200, 'msg': 'ok', 'data': data})
    # def post(self, request):
    #     user_id = request.data.get('user_id')
    #     print('>>>>>>>>>>>user_id', user_id)
    #     good = UserInfo.objects.filter(user_id=user_id)
    #     resp = UserInfoSerializer(good, many=True).data
    #     # sql = "select * from friend_login where user_id=%d" %(int(user_id))
    #     # resp = db1.find_all(sql)
    #     return Response({"code": 200, "message": "ok", "resp": resp})


class RenameNickName(APIView):
    """
    重命名好友备注
    """

    def post(self, request):
        nick_name = request.data.get('nick_name')
        user_id = request.query_params.get('user_id')
        print('>>>>>>>>>>>user_id', user_id)
        friend_id = request.data.get('friend_id')
        print('>>>>>>>>>>>friend_id', friend_id)
        try:
            users = UserInfo.objects.filter(user_id=user_id, friend_id=friend_id)
            print('>>>>>>>>.users', users)
            if users:
                users.update(nick_name=nick_name)
                return Response({'msg': '修改成功成功', 'code': 200})
            else:
                return Response({'msg': '修改失败', 'code': 403})
        except:
            error = traceback.format_exc()
            return Response({'code': 500, 'msg': error})


class GetUserMe(ListAPIView):
    """
    查看个人信息
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        print('>>>>>>>>>>>user_id', user_id)
        friend = User.objects.filter(id=user_id)
        data = UserSer(friend, many=True).data
        return Response({"code": 200, 'msg': 'ok', 'data': data})


class GetUserView(ListAPIView):
    """
    获取user表的所有数据
    """
    queryset = User.objects.all()
    serializer_class = UserSer


# 解绑三方登录
class Unbind(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        user = User.objects.get(username=username)
        if not user:
            return Response({'msg': '没有该绑定的账号', 'code': 400})
        user_id = user.id
        print("user_id绑定账号的user_id", user_id)
        oath_user = OauthUser.objects.get(user_id=user_id)
        if not oath_user:
            return Response({'msg': '你没有绑定,或者绑定已经解绑', 'code': 400})
        OauthUser.objects.filter(user_id=user_id)
        return Response({'msg': '解绑成功', 'code': 200})


# 编辑签名
class UpdateAutograph(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        autograph = request.data.get('autograph')
        user_id = request.query_params.get('user_id')
        users = User.objects.filter(id=user_id)
        if not users:
            return Response({"code": 400, "message": "No such person found"})
        else:
            users.update(autograph=autograph)
            return Response({'code': 200, 'msg': '修改成功'})


class QiNiuYun(APIView):
    """
    获取七牛云token
    """

    def get(self, request):
        return Response({'code': 200, 'token': get_qiniu_token()})


class UserInformationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user_id = user.id
        result = UserForm(request.data)
        # 启动校验
        logger.info('1111111111{}'.format(result.is_valid()))
        logger.info('正确的信息{}'.format(result.clean()))
        logger.info('错误的信息{}'.format(result.errors.as_json()))
        result_data = result.cleaned_data
        user_message = UserInformation.objects.filter(user_id=user_id).first()
        if not user_message:
            users = UserInformation.objects.create(user_id=user_id, **result_data)
            users.save()
            return Response({'code': 200, 'msg': '添加成功'})
        user = UserInformation.objects.get(user_id=user_id)
        for i in result_data.keys():
            # 修改性别
            if i == 'gender':
                if user.gender:
                    user.gender = result_data['gender']
                else:
                    return Response({'code': 400, 'msg': '不能修改性别'})
            # 修改出生日期
            if i == 'birthday':
                if user.birthday:
                    user.birthday = result_data['gender']
                else:
                    return Response({'code': 400, 'msg': '不能修改出生日期'})
            # 修改头像
            if i == 'image':
                user.image = result_data['image']
            # 修改简介
            if i == 'autograph':
                user.autograph = result_data['autograph']
            # 修改昵称
            if i == 'user_name':
                user.user_name = result_data['user_name']
                user.save()
        return Response({'code': 200, 'msg': '修改成功'})


class GetInformation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_id = user.id
        information = UserInformation.objects.filter(user_id=user_id)
        information_data = UserInformationSerializer(information, many=True).data
        logger.info('information_data:{}'.format(information_data))
        return Response({"msg": '获取成功', "code": 200, "data": information_data})


# 解绑
class UnbindPhone(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user_id = user.id
        user_phone = user.phone
        logger.info('user_id:{}'.format(user_id))
        phone = request.data.get('phone')
        code = request.data.get('code')
        logger.info('code:{}'.format(code))
        if phone != user_phone:
            return Response({'msg': '电话号码和数据库的手机号不一致', 'code': 400})
        # 校验短信验证码
        client = redis.Redis()
        sms_codes = client.get('sms_%s' % phone).decode()
        logger.info('sms_codes:{}'.format(sms_codes))
        # 校验验证码是否过期
        if not sms_codes:
            return Response({'msg': '验证码过期请重新登陆', "code": '204'})
        # 校验验证码是否正确
        if sms_codes != code:
            return Response({'msg': '验证码错误请重新输入', "code": '401'})
        user = User.objects.filter(id=user_id).update(phone='')
        user.save()
        logger.info('user:{}'.format(user))
        return Response({'msg': '解绑手机号成功', 'code': 200})


class BindPhone(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user_id = user.id
        user_phone = user.phone
        logger.info('user_id:{}'.format(user_id))
        phone = request.data.get('phone')
        code = request.data.get('code')
        logger.info('code:{}'.format(code))
        if user_phone != '':
            return Response({'msg': '该用户已经存在手机号', 'code': 400})
        phone_num = User.objects.filter(phone=phone).count()
        if phone_num != 0:
            return Response({'msg': '该用户的手机号已经被注册', 'code': 500})
        # 校验短信验证码
        client = redis.Redis()
        sms_codes = client.get('sms_%s' % phone).decode()
        logger.info('sms_codes:{}'.format(sms_codes))
        # 校验验证码是否过期
        if not sms_codes:
            return Response({'msg': '验证码过期请重新登陆', "code": '204'})
        # 校验验证码是否正确
        if sms_codes != code:
            return Response({'msg': '验证码错误请重新输入', "code": '401'})
        users = User.objects.filter(id=user_id).update(phone=phone)
        users.save()
        logger.info('users:{}'.format(users))
        return Response({'msg': '绑定手机号成功', 'code': 200})


# 绑定邮箱
class BindingEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user_id = user.id
        user_email = user.email
        email = request.data.get('email')
        code = request.data.get('code')
        print('code', code)
        print('user.email', email)
        if all([user_email]):
            return Response({"msg": '该用户的邮箱已经绑定', 'code': 400})
        rds = redis.Redis()
        sms_code = rds.get(email).decode('utf-8')
        logger.info('sms_code:{}'.format(sms_code))
        if not sms_code:
            return Response({"msg": '验证码不存在,请重新输入', 'code': 400})
        if sms_code != code:
            return Response({'msg': '验证码错误，请重新输入', 'code': 400})
        user.email = email
        user.save()
        logger.info('user:{}'.format(user))
        return Response({'msg': '绑定成功', 'code': 200})


def unbind_email(email):
    print('email', email)
    data = random.randint(100000, 999999)
    print('data', data)
    subject = '绑定邮箱'
    message = "绑定邮箱验证码:{}".format(data)
    from_email = '2457304066@qq.com'
    to_email = [email]
    print('to_email', to_email)
    send_email1(subject, message, from_email, to_email)
    print('发送成功')
    redis1 = redis.Redis()
    redis1.setex(email, 3600, data)


# 发送
class SendEmail(APIView):
    def post(self, request):
        email = request.data.get('email')
        print(email)
        unbind_email(email)
        return Response({'msg': '发送绑定验证成功'})


# 解绑邮箱
class UnbindEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user_id = user.id
        email = request.data.get('email')
        try:
            subject = '解绑邮箱'  # 邮件名
            message = '恭喜您解绑邮箱成功'  # 邮件内容
            from_email = '2457304066@qq.com'  # 发送人
            recipient_list = [email]  # 收件人
            msg = EmailMessage(subject, message, from_email, recipient_list)
            msg.send()
            User.objects.filter(id=user_id).update(email="")
            return Response({"code": 200, "message": "ok"})
        except:
            error = traceback.format_exc()
            logger.info('error:{}'.format(error))
            return Response({"code": 400, "error": error})


class GetAllUserGroup(generics.GenericAPIView):
    """
    获取所有的角色数据
    """
    serializer_class = UserGroupInfoSerializer
    # TODO 增加自定义权限
    permission_classes = [permissions.IsAuthenticated]
    query_param = []

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        group_list = UserGroup.objects.all()
        data = self.get_serializer(group_list, many=True).data
        return Response({'code': 200, 'data': data})


# class GetUserGroup(generics.GenericAPIView):
#     """
#     获取权限内容
#     """
#     serializer_class = UserResourceSerializer
#     permission_classes = [permissions.IsAuthenticated, ]
#     query_param = []
#
#     @swagger_auto_schema(method='get', manual_parameters=query_param)
#     @action(methods=['get'], detail=False)
#     def get(self, request):
#         group_list = Resource.objects.all()
#         data = self.get_serializer(group_list, many=True).data
#         return Response({'code': 200, 'data': data})
class OneUserResource(generics.GenericAPIView):
    """
    获取指定用户的权限
    """
    serializer_class = UserUserGroupListSer
    permission_classes = [permissions.IsAuthenticated]

    query_param = [
        openapi.Parameter(name='user_id', in_=openapi.IN_QUERY, description="用户id", type=openapi.TYPE_STRING),
    ]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        data = request.query_params
        user_id = data.get('user_id')
        user = User.objects.get(id=user_id)
        print('>>>>>>>>>>>>user', user)
        data = self.get_serializer(user).data
        # user_group_list = data.user_group_list
        # print('>>>>>>>>>>>>user_group_list', user_group_list)
        user_group_list = []
        datas = data['user_group_list']
        print('>>>>>>>>>>>>>>Datas', datas)
        for i in datas:
            print(">>>>>>>>>>>>>>i['children']", i['children'])
            # user_group_list.append(i['user_group_list'])
            # print('>>>>>>>>>>user_group_list', user_group_list)
        return Response({'code': 200, 'data': i['children']})


class GetUserResource(generics.GenericAPIView):
    """
    获取指定用户的权限数据
    """
    serializer_class = UserUserGroupListSer
    permission_classes = [permissions.IsAuthenticated, ]

    query_param = [
        openapi.Parameter(name='user_id', in_=openapi.IN_QUERY, description="用户id", type=openapi.TYPE_STRING),
    ]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        data = request.query_params
        user_id = data.get('user_id')
        user = User.objects.get(id=user_id)
        print('>>>>>>>>>>>>user', user)
        data = self.get_serializer(user).data
        return Response({'code': 200, 'data': data})


class GetUserList(generics.GenericAPIView):
    """
    获取用户列表  可以按名字查询
    """
    serializer_class = UserSer
    permission_classes = [permissions.IsAuthenticated]

    query_param = [openapi.Parameter(name='q', in_=openapi.IN_QUERY, description="查询条件", type=openapi.TYPE_STRING),
                   openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="页数大小",
                                     type=openapi.TYPE_NUMBER),
                   openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页码", type=openapi.TYPE_NUMBER),
                   ]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        data = request.query_params
        q = data.get('q')
        if not q:
            result_list = User.objects.all().order_by('-id')
        else:
            result_list = User.objects.filter(username__contains=q).order_by('-id')

        total_count = result_list.count()

        # 实例化分页对象
        page_cursor = MyPagination()
        # 分页
        data_list = page_cursor.paginate_queryset(result_list, request, view=self)

        data_list = self.get_serializer(data_list, many=True).data
        result = {'code': 200, 'data': data_list, 'total_count': total_count}
        return Response(result)


class AddUserResource(generics.GenericAPIView):
    """
    增加指定用户的权限数据
    """
    serializer_class = UserUserGroupListSer
    permission_classes = [permissions.IsAuthenticated, ]

    query_param = [
        openapi.Parameter(name='user_id', in_=openapi.IN_QUERY, description="用户id", type=openapi.TYPE_STRING),
    ]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        data = request.query_params
        user_id = data.get('user_id')
        resource_id = request.data.get('resource_id')
        usergroup_id = request.data.get('usergroup_id')
        user = UserGroup.objects.get(user_id=user_id)
        print('>>>>>>>>>>>>user', user)
        data = self.get_serializer(user).data
        return Response({'code': 200, 'data': data})
