
from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=15, verbose_name="手机号")
    email = models.CharField(max_length=30, verbose_name="邮箱", null=True, blank=True)
    invitation = models.CharField(max_length=20, verbose_name="邀请码", null=True, blank=True)
    begin_time = models.DateTimeField(default=timezone.now, verbose_name='注册时间')
    invite_code = models.CharField(max_length=20, verbose_name="邀请码", null=True, blank=True)
    register_code = models.CharField(max_length=20, verbose_name="注册时填写的邀请码", null=True, blank=True)
    integral = models.IntegerField(verbose_name="积分", default=0)
    nickname = models.CharField(max_length=30, verbose_name="昵称", null=True, blank=True)
    # birth = models.DateTimeField(verbose_name='出生日期', null=True, blank=True)
    birth = models.CharField(max_length=30, verbose_name='出生日期', null=True, blank=True)
    head = models.CharField(max_length=168, verbose_name="头像", null=True, blank=True)
    signature = models.CharField(max_length=50, verbose_name="个性签名", null=True, blank=True)
    choices = ((0, 'nan'), (1, 'nv'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=choices, null=True)

    class Meta:
        db_table = "child_user"

    def __str__(self):
        return self.username


# from django.forms.widgets import DateInput
#
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('title', 'dob')
#         labels = {
#             'dob': ('D.O.B'),
#         }
#         widgets = {
#             'dob': DateInput(attrs={'type': 'date'})
#         }


class Resource(models.Model):
    """
    资源表
    """
    resource_name = models.CharField(max_length=30, verbose_name='名称', default='')
    url = models.CharField(max_length=168, verbose_name='角色资源地址', null=True, blank=True)
    status = models.IntegerField(verbose_name='角色资源状态', default=1)
    pid = models.IntegerField(verbose_name='子id', default=0)

    class Meta:
        db_table = 'child_resource'

    def __str__(self):
        return self.resource_name


class UserGroup(models.Model):
    """
    用户组
    """
    name = models.CharField(max_length=30, verbose_name='名称', default='')
    user = models.ManyToManyField(User)
    resource = models.ManyToManyField(Resource)

    class Meta:
        db_table = 'child_user_group'

    def __str__(self):
        return self.name


class Friends(models.Model):
    """
    朋友表
    """
    user_id = models.IntegerField(verbose_name="用户id")
    friend_id = models.ForeignKey(User, verbose_name="朋友id", on_delete=models.CASCADE, null=True, blank=True)
    # friend_id = models.IntegerField(verbose_name="朋友id")
    status = models.IntegerField(null=True, blank=True, default=0, verbose_name="0好友1黑名单")
    remark_name = models.CharField(max_length=20, verbose_name="朋友备注", null=True, blank=True)
    site_mail = models.ForeignKey("site_letter.SendAddFriendMail", on_delete=models.CASCADE, verbose_name='站内信id', null=True, blank=True)
    # site_mail = models.IntegerField(verbose_name='站内信id', null=True, blank=True)
    handle_status = models.IntegerField(verbose_name='是否添加为好友(0:同意,1:忽略,2:拒绝)', default=-1)

    class Meta:
        db_table = "child_friends"


# # 黑名单表
class Blacklist(models.Model):
    # friend_id = models.IntegerField(verbose_name="好友id",null=True)
    friend = models.ForeignKey(Friends, verbose_name="朋友id", on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(verbose_name="状态(1黑名单2移除黑名单)", default=1)

    class Meta:
        db_table = "child_blacklist"


class ChatRecord(models.Model):
    """
    聊天记录
    只记录1v1聊天
    """
    user_id = models.IntegerField(blank=True, null=True)
    friend_id = models.IntegerField(blank=True, null=True)
    content = models.TextField()
    create_time = models.DateTimeField(default=timezone.now)
    group_id = models.CharField(max_length=100, default='')

    class Meta:
            db_table = 'chat_record'
