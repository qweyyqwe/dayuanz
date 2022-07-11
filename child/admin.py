from django.contrib import admin

# Register your models here.
# from .models import User
from .models import User, Resource, UserGroup


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)  # 展示
    list_filter = ('username',)
    list_per_age = 20  # 分页
    search_fields = ('username',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('resource_name', 'url', 'status', 'pid')  # 展示
    list_filter = ('resource_name',)
    list_per_age = 20  # 分页
    search_fields = ('resource_name',)


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )  # 展示
    list_filter = ('name',)
    list_per_age = 20  # 分页
    search_fields = ('name',)

