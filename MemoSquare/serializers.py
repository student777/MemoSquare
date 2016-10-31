from rest_framework import serializers
from MemoSquare.models import Memo


class MemoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
    page = serializers.CharField(max_length=255, read_only=True)
    timestamp = serializers.DateTimeField(format='%x %X', read_only=True)
    is_private = serializers.CharField(max_length=4)  # materialize form is fuck
    clipper = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'content', 'owner', 'page', 'clipper', 'is_private', 'timestamp')
