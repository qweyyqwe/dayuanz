# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : song_code.py
# @Software: PyCharm

from rest_framework.response import Response

from utils.phone_charm.phone_charm import send_message


def send_son(phone):
    # 调用方法
    result = send_message.delay(phone)
    if result['statusCode'] == '172001':
        return '网络错误'
    elif result['statusCode'] == '160038':
        return '验证码过于频繁'
    else:
        return 'ok  ok  ok!'
