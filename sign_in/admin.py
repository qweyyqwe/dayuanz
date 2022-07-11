from django.contrib import admin

# Register your models here.

from sign_in.models import Reward


@admin.register(Reward)
class AccountAdmin(admin.ModelAdmin):
    """
    账号后台管理
    """
    list_display = ('days', 'reward_coin', 'extra_reward', )  # 展示
    list_filter = ('days', 'reward_coin', 'extra_reward', )
    list_per_page = 20  # 分页
    search_fields = ('days', 'reward_coin', 'extra_reward', )
