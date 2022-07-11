from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    # 注册 账号 密码 手机号 验证码
    path('register/', views.RegisterView.as_view()),
    # 普通登录 账号 密码
    path('login_pass/', obtain_jwt_token, name='login'),
    # path('login_pass/', views.LoginCommonView.as_view()),
    # 手机号登录 验证码
    path('login_phone/', views.LoginPhoneView.as_view()),
    # 发送短信验证码
    path('send_sms/', views.SendSMSCode.as_view()),

    # 邮箱找回密码
    # 获取email
    path('get_email/', views.GetEmail.as_view()),
    # code的回调
    path('pass_code/', views.PassCode.as_view()),
    # 通过邮箱修改密码
    path('update_pass/', views.PutPass.as_view()),

    # 手机号找回密码
    # 获取手机号
    path('get_phone/', views.GetPhone.as_view()),
    # 手机号修改密码
    path('update_phone_pass/', views.PutPhonePass.as_view()),
    path('dingding/', views.DingDingCallBack.as_view()),
    path('dingding/bind/', views.BindDingDing.as_view()),
    path('add_friend/', views.AddFriend.as_view()),
    path('del_friend/', views.DeleteFriend.as_view()),
    path('rename/', views.RenameNickName.as_view()),

    path('list_friend/', views.GetFriend.as_view()),
    path('search_friend/', views.SearchFriend.as_view()),
    path('invitation_code/', views.InvitationCodeView.as_view()),
    path('code/', views.CodeViews.as_view()),
    path('code_register/', views.CodeLogin.as_view()),
    path('user_list/', views.GetUserView.as_view()),
    path('update_autograph/', views.UpdateAutograph.as_view()),
    path('user_me/', views.GetUserMe.as_view()),
    path('user_information/', views.UserInformationView.as_view()),
    path('get_information/', views.GetInformation.as_view()),
    # 解绑手机号
    path('unbind_phone/', views.UnbindPhone.as_view()),
    # 绑定手机号
    path('bind_phone/', views.BindPhone.as_view()),
    # 绑定邮箱
    path('unbind_email/', views.UnbindEmail.as_view()),
    path('binding/', views.BindingEmail.as_view()),
    path('send_email/', views.SendEmail.as_view()),
    # 获取用户的资源列表
    path('get_user_resource/', views.GetUserResource.as_view()),
    path('get_user_list/', views.GetUserList.as_view()),
    path('get_user_group/', views.GetAllUserGroup.as_view()),
    path('one_user/', views.OneUserResource.as_view()),

]
