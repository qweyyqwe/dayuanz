from django.db import models
from django.utils import timezone
from user.models import User


class PypMoments(models.Model):
    """朋友圈"""
    content = models.CharField(max_length=1000, verbose_name='朋友圈内容')
    create_time = models.DateTimeField(default=timezone.now(), verbose_name='发布时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id')

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'pyp_moments'
        verbose_name_plural = '朋友圈'


class PypPicture(models.Model):
    """朋友圈"""
    url = models.CharField(max_length=256, verbose_name='图片地址', default='')
    create_time = models.DateTimeField(default=timezone.now(), verbose_name='发布时间')
    moments = models.ForeignKey(PypMoments, on_delete=models.CASCADE, verbose_name='朋友圈')

    def __str__(self):
        return self.moments

    class Meta:
        db_table = 'pyp_picture'
        verbose_name_plural = '朋友圈图片'


class PypComment(models.Model):
    """朋友圈评论"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id')
    moments = models.ForeignKey(PypMoments, on_delete=models.CASCADE, verbose_name='朋友圈')
    content = models.CharField(max_length=200, verbose_name='评论内容')
    create_time = models.DateTimeField(default=timezone.now(), verbose_name='发布时间')
    pid = models.IntegerField(default=0, verbose_name='评论的id')

    def __str__(self):
        return self.pid

    class Meta:
        db_table = 'pyp_comment'
        verbose_name_plural = '朋友圈评论'
