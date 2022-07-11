from django.db import models

# Create your models here.
from child.models import User


class Reward(models.Model):
    """
    签到奖励列表
    """
    days = models.IntegerField(default=1, verbose_name='签到的天数')
    reward_coin = models.IntegerField(default=0, verbose_name='奖励积分数量')
    extra_reward = models.IntegerField(default=0, verbose_name='额外积分奖励')

    class Meta:
        """
        重命名
        """
        db_table = 'sign_in_reward'


class DailySignIn(models.Model):
    """
    用户签到信息表
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='签到用户')
    count_days = models.IntegerField(default=0, verbose_name='累计签到天数')
    continuous_day = models.IntegerField(default=0, verbose_name='连续签到天数')
    sign_in_time = models.DateTimeField(null=True, blank=True, verbose_name='签到时间')

    class Meta:
        """
        重命名
        """
        db_table = 'sign_in_daily'


