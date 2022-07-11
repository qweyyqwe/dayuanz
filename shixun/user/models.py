from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=11, verbose_name='手机号', unique=True, null=True)
    code = models.CharField(verbose_name="邀请码", max_length=255, unique=True, null=True)
    integral = models.IntegerField(verbose_name='积分', default=0)
    autograph = models.CharField(max_length=255, verbose_name='个性签名')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username


class OauthUser(models.Model):
    """
    第三方登录表(微信登录/qq登录/微博登录)
    """
    __tablename__ = 'oauth_user'
    image = models.CharField(max_length=255, verbose_name='头像', unique=True, null=True)
    uid = models.CharField(max_length=255, verbose_name='第三方登录的id', unique=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    oauth_type = models.CharField(max_length=255, verbose_name='第三方登录类型')

    class Meta:
        db_table = 'oauth_user'

    def __str__(self):
        return self.uid

    @classmethod
    def is_bind_user(cls, uid, oauth_type):
        """
        是否绑定用户
        """
        oauth = OauthUser.objects.filter(uid=uid, oauth_type=oauth_type).first()
        if oauth:
            return True
        return False


class UserInfo(models.Model):
    """
    好友列表
    """
    user_id = models.IntegerField(blank=True, null=True)
    friend_id = models.IntegerField(blank=True, null=True)
    nick_name = models.CharField(max_length=255, verbose_name='好友备注')

    class Meta:
        db_table = 'user_info'

    def __str__(self):
        return self.nick_name


class InvitationCode(models.Model):
    code = models.CharField(verbose_name="邀请码", max_length=10, unique=True)
    expires = models.DateTimeField(verbose_name="过期时间")

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'user_invitation_code'


class Resource(models.Model):
    name = models.CharField(max_length=30, verbose_name='名称', default='')
    url = models.CharField(max_length=256, verbose_name='角色资源地址', default='')
    status = models.IntegerField(verbose_name='角色资源状态', default=1)
    pid = models.IntegerField(verbose_name='父类id')

    class Meta:
        db_table = 'resource'

    def __str__(self):
        return self.name


class UserGroup(models.Model):
    """用户组的模型类"""
    name = models.CharField(max_length=30, verbose_name='名称', default='')
    user = models.ManyToManyField(User)
    # 更改模型类: 从多对一改为多对多
    resource = models.ManyToManyField(Resource)

    class Meta:
        db_table = 'user_group'

    def __str__(self):
        return self.name


class UserInformation(models.Model):
    choices = (
        (1, '男'), (2, '女'), (3, '其他')
    )
    user_name = models.CharField(max_length=30, verbose_name='昵称')
    image = models.CharField(max_length=256, verbose_name='头像')
    gender = models.IntegerField(choices=choices)
    autograph = models.CharField(max_length=255, verbose_name='个性签名')
    birthday = models.DateTimeField(verbose_name="出生日期")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")

    class Meta:
        db_table = 'user_information'

    def __str__(self):
        return self.user_name
