from rest_framework import serializers
from MemoSquare.models import Memo


class MemoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    page = serializers.CharField(max_length=255)
    timestamp = serializers.DateTimeField(format='%x %X', read_only=True)

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'content', 'owner', 'page', 'clipper', 'is_private', 'timestamp')
