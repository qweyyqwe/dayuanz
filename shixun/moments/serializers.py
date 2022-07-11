from dynamic.models import Dynamic
from .models import *
from rest_framework import serializers


class PypMomentsSer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.username

    class Meta:
        model = PypMoments
        fields = "__all__"


class PyqPictureSer(serializers.ModelSerializer):
    """
    朋友圈动态序列化器
    """
    picture_list = serializers.SerializerMethodField()

    class Meta:
        model = PypMoments
        fields = "__all__"

    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.username

    def get_picture_list(self, obj):
        """
        获取朋友圈图片列表
        :param obj:
        :return:
        """
        return PypPicture.objects.filter(moments_id=obj.id).values_list('url', flat=True)


class PypCommentSer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.username

    class Meta:
        model = PypComment
        fields = "__all__"
