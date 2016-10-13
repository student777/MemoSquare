from rest_framework import serializers
from MemoSquare.models import Memo


class MemoSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    page_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    title = serializers.CharField(required=False, allow_blank=True, max_length=255)
    content = serializers.CharField(style={'base_template': 'textarea.html'})
    dom_location = serializers.CharField(required=False, allow_blank=True, max_length=255)
    is_private = serializers.BooleanField(required=False)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Memo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.dom_location = validated_data.get('dom_location', instance.dom_location)
        instance.is_private = validated_data.get('is_private', instance.is_private)
        instance.save()
        return instance
