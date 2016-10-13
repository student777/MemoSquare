from rest_framework import serializers
from MemoSquare.models import Memo
from django.contrib.auth.models import User


class MemoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Memo
        fields = ('id', 'title', 'content', 'dom_location', 'is_private', 'owner', 'page')


class UserSerializer(serializers.ModelSerializer):
    memo = serializers.PrimaryKeyRelatedField(many=True, queryset=Memo.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'memo')
