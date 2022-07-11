# import jwt
#
#
# class Jwt:
#     def __init__(self):
#         self.secret = '%^&*qwertyuiop%^&%%^'
#
#     def encode_token(self, data):
#         return jwt.encode(data, self.secret, algorithm='HS256')
#
#     def decode_token(self, token):
#         return jwt.decode(token, self.secret, algorithms='HS256')
#
#     def checked_token(self, tokens):
#         payload = jwt.decode(tokens, self.secret, algorithms='HS256')
#         token = jwt.encode(payload, self.secret, algorithm='HS256')
#         if token == tokens:
#             return True
#         return False
#
#
# jwt_token = Jwt()
import logging
from django import forms
from rest_framework.permissions import BasePermission

from user.models import UserGroup
from user.serializers import ResourceSer

logger = logging.getLogger('log')


class IsCheckerPermission(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        user = request.user
        # 根据自己的需求，去进行用户权限的认证
        logger.info('IsChecker:{}'.format(user.is_superuser))
        if user.is_superuser:
            return True
        return False


class UserForm(forms.Form):
    image = forms.CharField(max_length=255, error_messages={"requird": "用户名不能为空", "min_length": "最小长度为255"}, required=True)
    autograph = forms.CharField(max_length=255, error_messages={"requird": "用户名不能为空", "min_length": "最小长度为255"}, required=True)
    gender = forms.IntegerField(error_messages={"requird": "性别无法修改"})
    user_name = forms.CharField(max_length=30, error_messages={"requird": "用户名不能为空", "min_length": "最小长度为5"}, required=True)
    birthday = forms.DateTimeField(required=False)


