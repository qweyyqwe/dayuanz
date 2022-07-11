from django.db import models
from django.utils import timezone

# Create your models here.
from child.models import User


class WeChatMoments(models.Model):
    """
    朋友圈记录 TODO 补充   审核——点赞——谁可见
    """
    userid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="发布者")
    content = models.CharField(max_length=268, verbose_name="朋友圈内容")
    begin = models.DateTimeField(default=timezone.now, verbose_name="发布时间")

    class Meta:
        db_table = "f_circle_wechatmoments"


class WeChatPicture(models.Model):
    """
    朋友圈图片表
    """
    moment_id = models.ForeignKey(WeChatMoments, on_delete=models.CASCADE, verbose_name="朋友圈id")
    url = models.CharField(max_length=168, verbose_name="图片路径")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        db_table = "f_circle_wechatpicture"


class WeChatComment(models.Model):
    """
    朋友圈评论
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论人")
    moment_id = models.ForeignKey(WeChatMoments, on_delete=models.CASCADE, verbose_name="朋友圈id")
    content = models.CharField(max_length=168, verbose_name="评论内容")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="评论时间")
    drop_time = models.DateTimeField(verbose_name="评论时间", null=True, blank=True)
    start = models.IntegerField(verbose_name="状态0显示/    1删除", null=True, blank=True, default=0)
    pid = models.IntegerField(verbose_name="父id", null=True, blank=True)

    class Meta:
        db_table = "f_circle_wechatcomment"
