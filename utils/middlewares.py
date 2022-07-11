# encoding: utf-8
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from child.models import User
from utils.resource import get_resource_list, menu_left_list


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
            resource_list = get_resource_list(user)
            menu_list = menu_left_list(resource_list)
            superuser = str(user.is_superuser)
            return {'code': 200, 'data': {'resource_list': menu_list, 'superuser': superuser, 'token': token,
                                          'user_id': user.id, 'username': user.username}}
            # return {'code': 200, 'data': {'resource_list': menu_list, 'superuser': superuser, 'token': token,
            #                               'user_id': user.id, 'username': user.username}}
        return {'code': 500, 'message': '用户已经被禁用'}
    # 否则就是用户名、密码有误
    return {'code': 406, 'message': '用户名或者密码错误'}

