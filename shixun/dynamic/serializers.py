from .models import *
from rest_framework import serializers


class DynamicSer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.username

    class Meta:
        model = Dynamic
        fields = "__all__"
