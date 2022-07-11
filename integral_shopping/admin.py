from django.contrib import admin

# Register your models here.
from .models import PointsMall, Img


@admin.register(PointsMall)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 展示
    list_filter = ('name',)
    list_per_age = 20  # 分页
    search_fields = ('name',)
