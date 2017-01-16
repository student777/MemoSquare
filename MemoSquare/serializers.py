from rest_framework import serializers
from MemoSquare.models import Memo, Category, Comment


class MemoSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='user.get_full_name', read_only=True)
    page = serializers.CharField(max_length=255, read_only=True)
    timestamp = serializers.DateTimeField(format='%b %d, %Y', read_only=True)
    category = serializers.CharField(max_length=45, allow_blank=True)

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'content', 'owner', 'page', 'is_private', 'timestamp', 'category')

    def to_representation(self, instance):
        json = super().to_representation(instance)

        # Add extra field
        json['num_clips'] = instance.clips.count()
        json['owner_pic_url'] = instance.user.detail.img_url
        json['num_comments'] = instance.comment.count()
        json['num_likes'] = instance.likes.count()

        # The reason why MemoSerializer's context field is required
        if 'user' in self.context:
            user = self.context['user']
            is_owner = user == instance.user
            json['is_clipped'] = user in instance.clips.all()
            json['is_owner'] = is_owner
            json['is_like'] = user in instance.likes.all()
        return json


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['pk', 'name']

    def validate(self, data):
        # When Category is created, check unique_together constraint
        if 'user' in self.context:
            user = self.context['user']
            if Category.objects.filter(user=user, name=data['name']).exists():
                raise serializers.ValidationError('That category name already exists')
        return data


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='user.get_full_name', read_only=True)
    memo = serializers.IntegerField(source='memo.pk', read_only=True)
    timestamp = serializers.DateTimeField(format='%b %d, %Y', read_only=True)

    class Meta:
        model = Comment
        fields = ['pk', 'memo', 'owner', 'content', 'timestamp']

    def to_representation(self, instance):
        json = super().to_representation(instance)

        # Add extra field
        json['num_likes'] = instance.like.count()

        if 'user' in self.context:
            user = self.context['user']
            is_owner = user == instance.user
            json['is_owner'] = is_owner
            json['is_like'] = user in instance.like.all()
