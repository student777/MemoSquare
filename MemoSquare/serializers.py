from rest_framework import serializers
from MemoSquare.models import Memo


class MemoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
    page = serializers.CharField(max_length=255, read_only=True)
    timestamp = serializers.DateTimeField(format='%b %d, %Y', read_only=True)
    is_private = serializers.BooleanField()

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'content', 'owner', 'page', 'is_private', 'timestamp')

    def to_representation(self, instance):
        json = super().to_representation(instance)

        # The reason why MemoSerializer's context field is required in ListView, DetailView
        if 'user' in self.context:
            user = self.context['user']
            is_clipped = user in instance.clipper.all()
            is_owner = user == instance.owner
            num_clips = instance.clipper.count()
            json['is_clipped'] = is_clipped
            json['is_owner'] = is_owner
            json['num_clips'] = num_clips
        return json
