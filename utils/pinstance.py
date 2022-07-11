# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : pinstance.py
# @Software: PyCharm
from rest_framework.pagination import PageNumberPagination


class PinstanceList(PageNumberPagination):
    """
    自定义分页器
    """
    page_size = 10

    page_size_query_param = 'size'

    page_query_param = 'page'

    max_page_size = 10
