from rest_framework import serializers
from MemoSquare.models import Memo


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ('id', 'title', 'content', 'user', 'page', 'com_location', 'is_private')
