from django.forms import model_to_dict

from .models import *
from rest_framework import serializers


class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserUserGroupListSer(serializers.ModelSerializer):
    user_group_list = serializers.SerializerMethodField()
    class Meta:
        """
        序列化模型
        """
        model = User
        fields = '__all__'

    def get_user_group_list(self, obj):
        # 获取该用户的角色列表
        user_group_list = obj.usergroup_set.all()
        result_list = []
        for user_group in user_group_list:
            # role ---》 obj对象
            # 获取当前角色的所有权限资源
            resource_query_list = user_group.resource.all()
            # 将对应的权限资源数据格式化
            resource_list = []
            for i in resource_query_list:
                if i.status == 1:
                    data = model_to_dict(i)
                    data.update({'tid': int(str(user_group.id) + str(i.id))})
                    resource_list.append(data)
            result_list.append({
                'id': user_group.id,
                'name': user_group.name,
                'children': resource_list,
                'tid': user_group.id
            })
        return result_list


class UserGroupInfoSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    tid = serializers.SerializerMethodField()

    class Meta:
        """
        序列化模型
        """
        model = UserGroup
        fields = ['id', 'name', 'children', 'tid']

    def get_tid(self, obj):
        return obj.id

    def get_children(self, obj):
        resource_query_list = obj.resource.all()
        resource_list = []
        for i in resource_query_list:
            if i.status == 1:
                data = model_to_dict(i)
                data.update({'tid': int(str(obj.id) + str(i.id))})
                resource_list.append(data)
        return resource_list


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"


class UserInformationSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    birthday = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    gender = serializers.CharField(source='get_gender_display')

    class Meta:
        model = UserInformation
        fields = "__all__"


class ResourceSer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class UserResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"
