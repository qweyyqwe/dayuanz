# from django.utils.deprecation import MiddlewareMixin
# from user.utils import Jwt
#
# from user.models import User
#
# obj_jwt = Jwt()
#
#
# class AuthMiddlware(MiddlewareMixin):
#     """解析token"""
#
#     def process_request(self, request):
#         """视图执行前"""
#         token = request.headers.get('Authorization')
#         print('>>>>>>>>>>>.token', token)
#         if token:
#             try:
#                 # 解密token decode
#                 jwt_token = obj_jwt.decode_token(token)
#                 print('>>>>>>>>>jwt_token', jwt_token)
#                 user = User.objects.get(username=jwt_token.get('username'))
#                 print('22222222222220', user)
#                 request.user = user
#             except Exception as e:
#                 print('22222222222222', e)
#                 return False
#         return
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from user.models import User


class AuthorBackend(ModelBackend):
    """
    重写登录注册的密码验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):

        user = User.objects.filter(Q(username=username) | Q(phone=username) | Q(email=username)).first()
        if user and user.check_password(password):
            return user
        return None


def jwt_response_payload_handler(token, user, request):
    if user is not None:
        if user.is_active:
            superuser = str(user.is_superuser)
            return {'code': 200, 'data': {'resource_list': [], 'superuser': superuser, 'token': token,
                                          'user_id': user.id, 'user_name': user.username}}
        return {'code': 500, 'message': '用户已经被禁用'}
    # 否则就是用户名、密码有误
    return {'code': 406, 'message': '用户名或者密码错误'}
