from rest_framework import serializers
from MemoSquare.models import Memo, Page
from django.contrib.auth.models import User


class MemoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    page = serializers.ReadOnlyField(source='page.url')

    class Meta:
        model = Memo
        fields = ('url', 'pk', 'title', 'content', 'dom_location', 'is_private', 'owner', 'page')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    memo = serializers.HyperlinkedRelatedField(many=True, view_name='memo-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'pk', 'username', 'email', 'memo')


class PageSerializer(serializers.HyperlinkedModelSerializer):
    memo = serializers.HyperlinkedRelatedField(many=True, view_name='memo-detail', read_only=True)

    class Meta:
        model = Page
        fields = ('url', 'pk', 'memo', )
