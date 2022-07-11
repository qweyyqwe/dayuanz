from django.utils import timezone
from django.db import models

# Create your models here.
from user.models import User


class Goods(models.Model):
    """
    商品表
    """
    name = models.CharField(max_length=30, verbose_name='商品名称')
    desc = models.CharField(max_length=100, verbose_name='商品描述', null=True, blank=True)
    image = models.CharField(max_length=300, verbose_name='商品图片', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField(default=0, verbose_name='库存数量')
    lock_count = models.IntegerField(default=0, verbose_name=' 锁定数量')
    sale_count = models.IntegerField(default=0, verbose_name='已售数量')

    class Meta:
        """
        重命名
        """
        db_table = 'goods'

    def get_available_count(self):
        """
        获取可用数据
        """
        return self.count - self.lock_count

    def add_lock_count(self, lock_count):
        """
        添加锁定数量
        """
        self.lock_count += lock_count
        self.save()

    def reduce_lock_count(self, lock_count):
        """
        减少锁定数量
        """
        self.lock_count -= lock_count
        self.save()

    def update_lock_count(self, count):
        """
        修改锁定数量
        锁定数量和销量一致
        """
        self.lock_count = count
        self.save()


class Picture(models.Model):
    """
    图片地址
    """
    url_path = models.CharField(max_length=256, verbose_name='图片地址', default='')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品id')

    class Meta:
        """
        重命名
        """
        db_table = 'goods_picture'


# 积分记录表
class GoodsRecord(models.Model):
    """积分记录表"""
    create_time = models.DateTimeField(default=timezone.now, verbose_name='积分兑换记录时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='商品id')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品id')
    price = models.IntegerField(verbose_name='积分', default=0)
    count = models.IntegerField(verbose_name='数量', default=1)

    class Meta:
        """
        重命名
        """
        db_table = 'goods_record'
