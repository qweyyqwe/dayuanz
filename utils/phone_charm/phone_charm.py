# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : phone_charm.py
# @Software: PyCharm


from ronglian_sms_sdk import SmsSDK
from celery import shared_task
# 导入随机模块
import random
import redis
import json

from utils.redis_cache import mredis

accId = '8aaf07087de13e49017dfedcbd0f062a'
accToken = '12dc48f628ca43a4888f4d752ad81779'
appId = '8a216da87de15752017dffb275fc06bb'
@shared_task
def send_message(mobile):
    sdk = SmsSDK(accId, accToken, appId)
    # 短信验证码的模板
    tid = '1'
    # mobile = '137'
    # 随机生成6位
    data = random.randint(100000, 999999)
    # 创建redis  客户端
    redis_cli = redis.Redis(host='47.111.69.97', port=6379, db=2)
    # 验证码写入redis  设置过期时间
    redis_cli.setex("sms_%s" % mobile, 60*7, data)
    # mredis.setex_str("sms_%s" % mobile, 60*7, data)
    # 转字典
    datas = (data, )
    resp = sdk.sendMessage(tid, mobile, datas)
    resps = json.loads(resp)
    return resps
