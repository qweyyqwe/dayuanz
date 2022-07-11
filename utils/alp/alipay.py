# -*- coding: utf-8 -*-
# @Time    : 2021/11/22
# @File    : com.py
# @Software: PyCharm


# 导入支付基类
from .pay import AliPay


# 初始化阿里支付对象
def get_ali_object():
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2021000119687640"  # APPID （沙箱应用）

    # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2() 接收不到这个请求
    notify_url = "http://localhost:8000/pay/callback/"

    # 支付完成后，跳转的地址。
    return_url = "http://localhost:8000/pay/callback/"
    # app_private_key_string = open("/private_key.txt").read()
    # alipay_public_key_string = open("/public_key.txt").read()
    merchant_private_key_path = r"utils\keys\private_key.txt"  # 应用私钥
    alipay_public_key_path = r"utils\keys\public_key.txt"  # 支付宝公钥
    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay
