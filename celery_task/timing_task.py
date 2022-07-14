import time
from email.mime.text import MIMEText

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from bank.models import LoanRecord
from bank.serializers import LoanRecordSer
from celery_task import celery_app
from goods.models import GoodsRecord
from django.core import mail


@celery_app.task(name='celery_task.timing_task.my_crontab')
def my_crontab(x, y):
    print(x, y)
    return x + y


@celery_app.task(name="celery_tasks.timing_task.my_times4")
def my_times4():
    data = time.strftime('%Y-%m-%d')
    num = GoodsRecord.objects.filter(create_time__contains=data).count()
    # if not num:
    #     return Response({"msg": "当天没有人兑换", "code": 400})
    subject = "每日商品数量"  # 邮件名
    message = render_to_string('index.html', {'num': num})  # 要跳的页面
    from_email = '2892694370@qq.com'  # 发送人
    recipient_list = ['l2892694370@163.com']  # 收件人
    msg = EmailMessage(subject, message, from_email, recipient_list)
    msg.content_subtype = 'html'  # 如果要发送html格式邮件，需要指定一下，如果发送普通邮件，无须这一行代码
    msg.send()
    print("9999", num)


@celery_app.task(name='celery_tasks.timing_task.every_bank_loan')
def every_bank_loan():
    loan_record = LoanRecord.objects.all()
    data = LoanRecordSer(loan_record, many=True).data
    subject = "每日贷款数据清单"  # 邮件名
    msg = render_to_string('index.html', {'data': data})
    message = MIMEText(msg, _subtype='html', _charset='utf-8')
    from_email = '2457304066@qq.com'  # 发送人
    recipient_list = ['2457304066@qq.com']  # 收件人
    mail.send_mail(subject, message, from_email, recipient_list)
