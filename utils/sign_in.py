# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : sign_in.py
# @Software: PyCharm
# 封装签到的方法


def check_time_is_same_daily(time1, time2):
    """
    判断2个时间是否为同一天
    :param time1:
    :param time2:
    :return: TRUE FALSE
    """
    # 如果期中一个参数为空，那么默认不是同一天
    if time1 and time2:
        if time1.strftime('%Y-%m-%d') == time2.strftime('%Y-%m-%d'):
            return True
        return False
    else:
        return False


def check_time_is_continue(time1, time2):
    """
    判断2个时间是否为连续的2天
    :param time1: 今天的时间
    :param time2: 上次签到时间
    :return: 连续 True  不连续 False
    """
    if time1 and time2:
        time3 = time1.replace(tzinfo=None) - time2.replace(tzinfo=None)
        if time3.days == 1:
            return True
        return False
    else:
        return True
