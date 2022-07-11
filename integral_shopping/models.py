from django.utils import timezone

from django.db import models
# Create your models here.
from child.models import User


class PointsMall(models.Model):
    """
    积分商城
    """
    name = models.CharField(max_length=30, verbose_name="商品名字", null=True, blank=True)
    desc = models.TextField(verbose_name="简介", null=True, blank=True)
    image = models.CharField(max_length=168, verbose_name="简介图片", null=True, blank=True)
    price = models.IntegerField(verbose_name="价格", default=0)
    count = models.IntegerField(verbose_name="库存", default=0)
    lock_count = models.IntegerField(verbose_name="锁定库存", default=0)
    sale_count = models.IntegerField(verbose_name="销量", default=0)
    status = models.IntegerField(verbose_name="状态0存在/   1下架", default=0)
    cateid = models.ForeignKey('Type', on_delete=models.CASCADE, verbose_name="商品类别", null=True, blank=True)

    class Meta:
        db_table = "integral_shopping_pointsmall"


class Img(models.Model):
    """
    图片表
    """
    pointsmallid = models.ForeignKey(PointsMall, on_delete=models.CASCADE, verbose_name="积分商城图片")
    url = models.CharField(max_length=168, verbose_name="url地址")

    class Meta:
        db_table = "integral_shopping_img"


class Type(models.Model):
    """
    类型
    """
    name = models.CharField(max_length=50, verbose_name="类型名", null=True, blank=True)

    class Meta:
        db_table = "integral_shopping_type"


class Record(models.Model):
    """
    积分记录表
    """
    create_time = models.DateTimeField(default=timezone.now, verbose_name='积分兑换记录时间')
    user_id = models.IntegerField(verbose_name='用户id', null=True, blank=True)
    goods_id = models.IntegerField(verbose_name='商品id', null=True, blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id', null=True, blank=True)
    # goods = models.ForeignKey(PointsMall, on_delete=models.CASCADE, verbose_name='商品id', null=True, blank=True)
    price = models.IntegerField(verbose_name='积分', null=True, blank=True)
    count = models.IntegerField(verbose_name='数量', null=True, blank=True)
    source = models.CharField(max_length=40, verbose_name="来源说明", null=True, blank=True)
    type = models.IntegerField(verbose_name="0是减少积分/    1添加积分", null=True, blank=True)

    class Meta:
        db_table = 'integral_shopping_record'











