import time

from django.core import mail

from celery_task import celery_app
from celery import shared_task
from ronglian_sms_sdk import SmsSDK
import random

accId = '8aaf07087f77bf96017fd54021082f71'
accToken = 'fcc9d94e2c324d32a93081fe8323c959'
appId = '8aaf07087f77bf96017fd54021ff2f78'


@shared_task()
def send_message(phone):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'  # 容联云分配的一个测试短信验证码模版
    # mobile = '18937774001'  # 接收短信的手机号
    data = '%06d' % random.randint(100000, 999999)
    datas = (data,)
    resp = sdk.sendMessage(tid, phone, datas)
    print('>>>>>>>>>>>>>>>>>', resp)
    print('>>>>>>>>>>>>>>>>>', data)
    return resp, data


if __name__ == '__main__':
    send_message()


@celery_app.task
def test(mobile, code):
    print('1111')
    time.sleep(15)
    return mobile + code


@celery_app.task(name='send_email1')
def send_email1(subject, message, from_email, to_email):
    time.sleep(3)
    mail.send_mail(subject, message, from_email, to_email)
    print('发送邮件')


@celery_app.task(name='send_email2')
def send_email2(subject, message, from_email, to_email):
    time.sleep(3)
    mail.send_mail(subject, message, from_email, to_email)
    print('发送到站邮件')


@celery_app.task(name='send_email')
def send_email(subject, message, from_email, to_email):
    time.sleep(3)
    mail.send_mail(subject, message, from_email, recipient_list=to_email)
    print('发送邮件')



