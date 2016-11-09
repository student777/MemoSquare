from rest_framework import serializers
from MemoSquare.models import Memo


class MemoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
    page = serializers.CharField(max_length=255, read_only=True)
    timestamp = serializers.DateTimeField(format='%b %d, %Y', read_only=True)
    is_private = serializers.BooleanField()

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'content', 'owner', 'page', 'is_private', 'timestamp', 'clipper')

    def to_representation(self, instance):
        json = super().to_representation(instance)

        if 'request' in self.context:
            request = self.context['request']
            is_clipped = request.user.pk in json['clipper']
            json['is_clipped'] = is_clipped
        return json
