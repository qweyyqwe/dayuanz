# -*- coding: utf-8 -*-
# @Time    : 2021/11/22
# @File    : com.py
# @Software: PyCharm

import traceback
import logging

from django.db import transaction
from rest_framework.response import Response

# 导入支付基类
from .pay import AliPay
from utils.alp.code import uniqueness_code
from utils.redis_cache import mredis
from django.shortcuts import redirect


logger = logging.getLogger('log')

# 初始化阿里支付对象
def get_ali_object():
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2021000119687640"  # APPID （沙箱应用）

    # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2() 接收不到这个请求
    # 通知商户用户支付成功与否的页面
    notify_url = "http://localhost:8000/bank/callback/"

    # 支付完成后，跳转的地址。  用户支付成功返回的页面
    return_url = "http://localhost:8000/bank/callback/"
    # app_private_key_string = open("/private_key.txt").read()
    # alipay_public_key_string = open("/public_key.txt").read()
    merchant_private_key_path = r"utils\alp\private_key.txt"  # 应用私钥
    alipay_public_key_path = r"utils\alp\public_key.txt"  # 支付宝公钥
    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay


def pay(money, id):
    with transaction.atomic():
        # 创建事务保存点
        save_id = transaction.savepoint()
        try:
            code = uniqueness_code(id)
            alipay = get_ali_object()
            query_params = alipay.direct_pay(
                subject="充值",  # 商品简单描述
                out_trade_no=code,  # 用户购买的商品订单号(每次都不一样)
                total_amount=int(money)  # 交易金额
            )
            # bank_user = BankUser.objects.get(user_id=user_id)
            # TopUpRecord.objects.create(user_id=bank_user.id, money=money, code=code)
            # bank_user.money += int(money)
            # bank_user.save()
            pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)
            # # 提交订单成功，显式的提交一次事务
            transaction.savepoint_commit(save_id)
            return pay_url
        except:
            # 报错回滚
            transaction.savepoint_rollback(save_id)
            error = traceback.format_exc()
            logger.error('GetMoney——error:{}'.format(error))
            return error



