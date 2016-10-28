from rest_framework import serializers
from MemoSquare.models import Memo


class MemoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    page = serializers.CharField(max_length=255)
    timestamp = serializers.DateTimeField(format='%x %X')
    # page = serializers.ReadOnlyField(source='page.url')
    # page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'content', 'owner', 'page', 'clipper', 'is_private', 'timestamp')
        read_only_fields = ('timestamp',)
