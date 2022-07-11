from django.db import models
from django.utils import timezone

from user.models import User


class Dynamic(models.Model):
    publish_time = models.DateTimeField(default=timezone.now(), verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='公告发布人', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=50)
    content = models.CharField(verbose_name='内容', max_length=50)
    ic_people = models.CharField(verbose_name='审核员', max_length=50)
    status = models.IntegerField(default=0, verbose_name='状态  0 审核中 1审核通过 2审核不通过')
    img = models.CharField(verbose_name='内容', max_length=256, blank=True, null=True)

    class Meta:
        db_table = 'dynamic'

    def __str__(self):
        return self.title


