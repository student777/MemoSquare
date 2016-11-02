from rest_framework import serializers
from MemoSquare.models import Memo


class MemoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
    page = serializers.CharField(max_length=255, read_only=True)
    timestamp = serializers.DateTimeField(format='%b %d, %Y', read_only=True)
    is_private = serializers.CharField(max_length=10)  # materialize form is fuck

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'content', 'owner', 'page', 'is_private', 'timestamp')
