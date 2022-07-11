from django.db import models

# Create your models here.


"""
站内信模型类
"""
'''
from django.db import models

from django.utils import timezone


# 信息类型表
class MessageType(models.Model):
    """
    消息内容
    """
    name = models.CharField(max_length=20, verbose_name='信息类型名称（动态、商城消息）')
    content = models.CharField(max_length=200, verbose_name='信息内容')
    title = models.CharField(max_length=20, verbose_name='信息标题')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='消息发送时间')
    site_mail_type = models.IntegerField(verbose_name='站内信消息类型（0全体/用户id）')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '信息内容'
        db_table = 'site_letter_message_content'


# class SiteMailType(models.Model):
#     """
#     站内信消息 群发消息表
#     """
#     content_id = models.IntegerField(verbose_name='消息内容，MessageContent中保存')
#     site_mail_type = models.IntegerField(verbose_name='站内信消息类型（0全体/用户id）')
#     create_time = models.DateTimeField(default=timezone.now, verbose_name='消息发送时间')
#
#     class Meta:
#         verbose_name_plural = '群发消息表'
#         db_table = 'site_letter_sitemailtype'


class SiteMail(models.Model):
    """
    站内信
    """
    # 为了提高表的查询速率，将表进行了垂直分割
    message_type = models.ForeignKey(MessageType, on_delete=models.CASCADE, verbose_name='信息内容')
    status = models.IntegerField(verbose_name='0未读1已读', default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '站内信息表'
        db_table = 'site_letter_mail'


'''
from django.db import models
from django.utils import timezone


class SendMail(models.Model):
    """
    发送站内信息
    """
    user = models.IntegerField(verbose_name='0代表全部人，user_id普通用户')
    content = models.CharField(max_length=256, verbose_name='信息内容')
    title = models.CharField(max_length=20, verbose_name='信息标题')

    content_id = models.IntegerField(verbose_name='消息内容，MailInfo中保存')
    site_mail_type = models.IntegerField(verbose_name='站内信消息类型（0全体/用户id）')
    send_time = models.DateTimeField(default=timezone.now, verbose_name='发布时间')

    class Meta:
        verbose_name_plural = '发送站内信息'
        db_table = 'site_letter_sendmail'


class MailInfo(models.Model):
    """
    站内信息内容
    """
    # 0未读 1 已读
    user = models.IntegerField(verbose_name='用户id')
    status = models.IntegerField(verbose_name='0未读1已读', default=0)
    send_mail = models.ForeignKey(SendMail, on_delete=models.CASCADE, verbose_name='站内信消息id')

    class Meta:
        verbose_name_plural = '站内信息内容'
        db_table = 'site_letter_mailinfo'


class SendAddFriendMail(models.Model):
    """
    发送添加好友站内信息
    """
    user = models.ForeignKey("child.User", on_delete=models.CASCADE, verbose_name='站内信消息user_id')
    content = models.CharField(max_length=256, verbose_name='信息内容')
    title = models.CharField(max_length=20, verbose_name='信息标题')
    send_time = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    friend_id = models.IntegerField(verbose_name='请求人id')
    status = models.IntegerField(verbose_name='处理结果(0:未处理,1:已处理)', default=0)

    class Meta:
        verbose_name_plural = '发送添加好友站内信息'
        db_table = 'site_letter_send_addfriendmail'


