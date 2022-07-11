from django.contrib import admin

# Register your models here.
# from .models import User
from .models import Plaza


@admin.register(Plaza)
class PlazaAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'check_content',)  # 展示
    list_filter = ('title', 'code', 'check_content',)
    list_per_age = 20  # 分页
    search_fields = ('title', 'code', 'check_content',)
