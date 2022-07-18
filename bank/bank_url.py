# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : plaza_url.py
# @Software: PyCharm


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('add_bank_user', views.AddBankUser.as_view(), name="add_bank_user"),
    path('add_plaza_user/', views.AddBankUser.as_view()),
    path('get_bank_user_info/', views.GetBankUserInfo.as_view()),
    # 借贷手机验证码
    path('get_bank_phone/', views.GetBankPhone.as_view()),
    # 借贷申请
    path('loan_money/', views.LoanMoney.as_view()),
    # 用户自己审核通过的
    path('show_bank_user/', views.ShowBankUser.as_view()),
    # 借贷未进行 分配的
    path('get_not_bank_money/', views.GetNotLoanMoney.as_view()),
    # 审核人获取自己需审核的数据
    path('all_loan_money_record/', views.GetAllLoanMoney.as_view()),
    path('succeed/', views.CheckSucceed.as_view()),
    # 充值调用 支付宝
    path('get_money/', views.GetMoney.as_view()),
    # 充值回调
    path('callback/', views.GoMoney.as_view()),

    path('get_sign_all/', views.ShowSignAll.as_view()),
    # 新标  投资
    path('invest_money/', views.InvestMoney.as_view()),
    # 投标回调
    path('callback/', views.InvestCallBack.as_view()),
    # 获取还款列表
    path('get_user_loan/', views.GetUserLoan.as_view()),
    # 还款
    path('refund_money/', views.RefundMoney.as_view()),
    path('send_refund_code/', views.SendRefundCode.as_view()),




]

