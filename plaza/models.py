# 用户发布的动态，评论

from django.db import models
from django.utils import timezone


class Plaza(models.Model):
    """
    动态表
    """

    # userid = models.ForeignKey(User, verbose_name="发布人id", on_delete=models.CASCADE)
    userid = models.IntegerField(verbose_name="发布人id")
    title = models.CharField(max_length=268, verbose_name="标题", null=True, blank=True)
    content = models.CharField(max_length=268, verbose_name="内容")
    code = models.CharField(max_length=50, verbose_name="唯一标识", null=True, blank=True)
    begin_time = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    over_time = models.DateTimeField(verbose_name='删除时间', null=True, blank=True)
    start = models.IntegerField(verbose_name="0显示/  1删除动态", default=0)
    checkid = models.IntegerField(verbose_name="审核人id", null=True, blank=True)
    check_start = models.IntegerField(verbose_name="0未审核    /1审核中   /2通过    /3失败", default=0)
    check_content = models.CharField(max_length=268, null=True, blank=True)

    class Meta:
        db_table = "plaza_plazas"


class Discuss(models.Model):
    """
    评论表
    """

    uid = models.IntegerField()  # 评论人或回复人
    # discuss_fatherid = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, verbose_name='父评论id')
    discuss_fatherid = models.IntegerField(null=True, blank=True)
    plazaid = models.IntegerField()  # 所属帖子
    content = models.CharField(max_length=268, verbose_name="评论内容")
    discuss_time = models.DateTimeField(default=timezone.now, verbose_name='评论时间')
    starts = models.IntegerField(verbose_name="0显示/ 1删除")

    class Meta:
        db_table = "plaza_discuss"
