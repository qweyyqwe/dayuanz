# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : custom_permissions.py
# @Software: PyCharm


from rest_framework.permissions import BasePermission

from child.views import logger


class IsCheckUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        return False


class IsPointsManagerPermission(BasePermission):
    """
    是否为积分商城管理员角色

    积分商城管理员的角色数据id为3
    """

    def has_permission(self, request, view):
        user = request.user
        # 获取当前用的角色id列表
        role_list = user.role_set.values_list('id',  flat=True)
        logger.info('IsPointsManagerPermission:{}'.format(role_list))
        if 3 in role_list:
            return True
        return False