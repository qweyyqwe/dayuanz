from django.contrib import admin
from .models import InvitationCode

from user.models import User, Resource, UserGroup


class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "expires")

    class Meta:
        model = InvitationCode


admin.site.register(InvitationCode, InvitationCodeAdmin)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)  # 展示
    list_filter = ('username',)
    list_per_age = 20  # 分页
    search_fields = ('username',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'pid', 'name', 'url', 'status',)  # lyy展示lyy
    list_filter = ('name', 'url', 'status',)
    list_per_age = 20  # 分页
    search_fields = ('name', 'url', 'status',)


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 展示
    list_filter = ('name',)
    list_per_age = 20  # 分页
    search_fields = ('name',)
