from rest_framework import serializers
from comment.models import Comment


class CommentSer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.username

    class Meta:
        model = Comment
        fields = "__all__"
