from rest_framework import serializers
from MemoSquare.models import Memo


class MemoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
    page = serializers.CharField(max_length=255, read_only=True)
    timestamp = serializers.DateTimeField(format='%b %d, %Y', read_only=True)

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'content', 'owner', 'page', 'is_private', 'timestamp')

    def to_representation(self, instance):
        json = super().to_representation(instance)

        # Add extra field
        num_clips = instance.clipper.count()
        owner_pic_url = instance.owner.detail.img_url
        json['num_clips'] = num_clips
        json['owner_pic_url'] = owner_pic_url

        # The reason why MemoSerializer's context field is required
        if 'user' in self.context:
            user = self.context['user']
            is_clipped = user in instance.clipper.all()
            is_owner = user == instance.owner
            json['is_clipped'] = is_clipped
            json['is_mymemo'] = is_owner  # fuck Konglish
        return json
