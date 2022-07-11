from dynamic.models import Dynamic
from .models import *
from rest_framework import serializers


class GoodsSer(serializers.ModelSerializer):
    # goods_name = serializers.SerializerMethodField()
    #
    # def get_goods_name(self, obj):
    #     return obj.goods.name

    class Meta:
        model = Goods
        fields = "__all__"


class GoodsRecordSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    goods_name = serializers.SerializerMethodField()

    def get_goods_name(self, obj):
        return obj.goods.name

    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = GoodsRecord
        fields = "__all__"
