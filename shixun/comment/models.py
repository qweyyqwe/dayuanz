from django.db import models

from dynamic.models import Dynamic
from user.models import User


class Comment(models.Model):
    """
    评论表

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dynamic = models.ForeignKey(Dynamic, on_delete=models.CASCADE)
    content = models.CharField(max_length=100, verbose_name='评论内容')
    status = models.IntegerField(default=1, verbose_name='1可用0不可用')
    pid = models.IntegerField(verbose_name='父id', default=0)

    class Meta:
        db_table = 'comment'
