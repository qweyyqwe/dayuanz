# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : child_url.py
# @Software: PyCharm


from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('register/', views.Register.as_view()),
    # 账号密码登录
    path('login_account/', views.LoginAccount.as_view()),
    # 重写登录视图
    path('login_token/', obtain_jwt_token, name="login"),
    # 手机号登录
    path('login_phone/', views.LoginPhone.as_view()),
    # 手机验证码
    path('code/', views.SmsCode.as_view()),
    # 发送图形验证码
    path('img/<uuid:uuid>/', views.ImgCode.as_view()),
    # 校验图形验证码
    path('check_img_code/', views.CheckImgCode.as_view()),
    # 发送邮箱
    path('email_song/', views.EmailSong.as_view()),
    # 修改密码
    path('put_secret/', views.PutPassword.as_view()),
    # TODO 搜索暂时——展示所有用户
    path('find_user/', views.FindUser.as_view()),
    # 添加好友
    path('add_friend/', views.AddFriends.as_view()),
    # path('show_user_friend/<int:user_id>/', views.ShowUserFriend.as_view()),
    # 展示用户对应下的好友
    path('show_user_friend/', views.ShowUserFriend.as_view()),
    # 聊天信息
    path('get_chat_record/', views.GetChatRecord.as_view()),
    # 修改好友
    path('put_friend_name/', views.PutFriendName.as_view()),
    path('invite/', views.Invite.as_view()),
    # form表单使用
    path('invites/', views.FormTestView.as_view()),
    # 权限
    path('get_user_group/', views.GetUserRolesList.as_view()),
    # 个人信息
    path('get_user_info/', views.GetUserInfo.as_view()),
    # # 完善信息/修改信息
    path('complete_user_info/', views.CompleteUserInfo.as_view()),
    # # 修改个人信息
    # path('update_user_info/', views.UpdateUserInfo.as_view()),
    # # 获取所有角色数据
    # path('get_all_role/', views.GetAllRole.as_view()),
    # # 获取所有资源
    # path('get_all_resource/', views.AllResource.as_view()),
    # # 签到
    # path('sign/', views.Sign.as_view()),
    # # 签到2   7天一循环签到
    # path('sign_server/', views.SignServer.as_view()),
    # 添加黑名单
    path('black_friend/', views.BlackFriend.as_view()),
    # # 展黑名单
    path('get_black_friend/', views.GetBlackFriend.as_view()),
    # # 移除黑名单
    # path('sign/', views.Sign.as_view()),

]
