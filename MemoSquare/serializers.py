from rest_framework import serializers
from MemoSquare.models import Memo, Category


class MemoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.get_full_name', read_only=True)
    page = serializers.CharField(max_length=255, read_only=True)
    timestamp = serializers.DateTimeField(format='%b %d, %Y', read_only=True)
    category = serializers.CharField(max_length=45, allow_blank=True)

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'content', 'owner', 'page', 'is_private', 'timestamp', 'category')

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


class CategorySerializer(serializers.ModelSerializer):

    def validate(self, data):
        # When Category is created, check unique_together constraint
        if 'user' in self.context:
            user = self.context['user']
            if Category.objects.filter(owner=user, name=data['name']).exists():
                raise serializers.ValidationError('That category name already exists')
        return data

    class Meta:
        model = Category
        fields = ['pk', 'name']
        extra_kwargs = {'owner': {'required': 'False'}}


class ImageSerializer(serializers.BaseSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)