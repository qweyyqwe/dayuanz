"""
存管系统
"""
from django.db import models
from django.utils import timezone

from child.models import User


# Create your models here.


class BankUser(models.Model):
    """
    开户账号
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联账号')
    name = models.CharField(max_length=100, verbose_name='用户姓名')
    card_id = models.CharField(max_length=18, verbose_name='身份证号')
    bank_card_id = models.CharField(max_length=100, verbose_name='银行卡号')
    password = models.CharField(max_length=6, verbose_name='用户银行卡密码')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='开户时间')
    money = models.IntegerField(default=0, verbose_name="余额")

    class Meta:
        db_table = 'bank_bankuser'


# class InvestRecord(models.Model):
#     """
#     投资表
#     """
#     user = models.ForeignKey(BankUser, on_delete=models.CASCADE, verbose_name='关联开户人员')
#     loan = models.ForeignKey('LoanRecord', on_delete=models.CASCADE, verbose_name='贷款理财')
#     create_time = models.DateTimeField(default=timezone.now, verbose_name='开户时间')
#     earnings_money = models.IntegerField(verbose_name="预收益", null=True, blank=True)
#
#     class Meta:
#         db_table = 'bank_investrecord'


class LoanRecord(models.Model):
    """
    贷款表
    """
    user = models.ForeignKey(BankUser, on_delete=models.CASCADE, verbose_name='关联开户人员')
    loan_money = models.IntegerField(verbose_name="贷款金额")
    # loan_money = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="贷款金额")
    loan_time = models.DateTimeField(default=timezone.now, verbose_name='贷款时间')
    late_time = models.DateTimeField(verbose_name='最晚还款贷款时间', null=True, blank=True)
    content = models.IntegerField(verbose_name="借贷描述", default=0)
    expect = models.IntegerField(verbose_name="分期", default=0)
    status = models.IntegerField(verbose_name="状态(0待审核/ 1审核中/   2审核通过/  3不通过/   4取消)", default=0)
    cause = models.TextField(verbose_name="不通过原因", default='')
    count = models.IntegerField(verbose_name="贷款次数", default=0)
    code = models.CharField(max_length=30, verbose_name="唯一标识", default='')
    check_user_id = models.IntegerField(verbose_name="审核人id", null=True, blank=True)
    loan_status = models.IntegerField(verbose_name="状态(0未审核/ 1筹备中/   2满标/)", default=0)

    class Meta:
        db_table = 'bank_loanrecord'


class TopUpRecord(models.Model):
    """
    充值记录表
    """
    user = models.ForeignKey(BankUser, on_delete=models.CASCADE, verbose_name='充值人员')
    money = models.IntegerField(verbose_name="充值金额", null=True, blank=True)
    code = models.CharField(max_length=30, verbose_name="生成唯一code", default='')
    serial_number = models.CharField(max_length=50, verbose_name="订单流水号", default='')
    create_time = models.DateTimeField(default=timezone.now, verbose_name="充值时间")
    status = models.IntegerField(verbose_name="状态(0成功/ 1网络错误/   2取消/)", null=True, blank=True)

    class Meta:
        db_table = 'bank_topuprecord'




