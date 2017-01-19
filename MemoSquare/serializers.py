from rest_framework import serializers
from MemoSquare.models import Memo, Category, Comment


class MemoSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)  # can't use slugRelated field because it doesn't support get_full_name
    page = serializers.SlugRelatedField(slug_field='url', read_only=True)
    timestamp = serializers.DateTimeField(format='%b %d, %Y', read_only=True)

    class Meta:
        model = Memo
        fields = ('pk', 'title', 'content', 'user', 'page', 'is_private', 'timestamp', 'category')

    def to_representation(self, instance):
        json = super().to_representation(instance)

        # Add extra field
        json['num_clips'] = instance.clips.count()
        json['owner_pic_url'] = instance.user.detail.img_url
        json['num_comments'] = instance.comment.count()
        json['num_likes'] = instance.likes.count()

        '''
        [trick] Change field name user->owner
        ref) http://stackoverflow.com/questions/37496584/changing-the-field-name-when-using-django-rest-framework
        Underscore cannot be used in Serializer field name
        '''
        json['owner'] = json['user']
        json['category_pk'] = json['category']
        del json['category']

        # The reason why MemoSerializer's context field is required
        if 'user' in self.context:
            user = self.context['user']
            is_owner = user == instance.user
            json['is_clipped'] = user in instance.clips.all()
            json['is_owner'] = is_owner
            json['is_liked'] = user in instance.likes.all()
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
    user = serializers.CharField(source='user.get_full_name', read_only=True)
    timestamp = serializers.DateTimeField(format='%b %d, %Y', read_only=True)
    memo = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['pk', 'memo', 'user', 'content', 'timestamp']

    def to_representation(self, instance):
        json = super().to_representation(instance)

        # Add extra field
        json['num_likes'] = instance.likes.count()
        json['owner_pic_url'] = instance.user.detail.img_url

        # Change field name
        json['owner'] = json['user']
        json['memo_pk'] = json['memo']
        del json['memo']

        if 'user' in self.context:
            user = self.context['user']
            is_owner = user == instance.user
            json['is_owner'] = is_owner
            json['is_liked'] = user in instance.likes.all()
        return json
