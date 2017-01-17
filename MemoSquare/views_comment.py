from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes, api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from MemoSquare.models import Comment, LikeComment
from rest_framework.renderers import JSONRenderer
from MemoSquare.serializers import CommentSerializer
from django.db.utils import IntegrityError


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes((permissions.IsAuthenticated,))
def list_create(request):
    if request.method == 'GET':
        memo_id = request.query_params['memo']
        query_set = Comment.objects.filter(memo_id=memo_id)
        serializer = CommentSerializer(query_set, many=True, context={'user': request.user})
        return Response(serializer.data)

    elif request.method == 'POST':
        memo_id = request.data['memo']
        serializer = CommentSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save(user=request.user, memo_id=memo_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes((permissions.IsAuthenticated,))
def update_delete(request, pk):
    # get comment object
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        data = {'msg': 'Comment does not exist'}
        return Response(data, status=status.HTTP_404_NOT_FOUND, template_name='error_msg.html')

    # permission check
    if comment.user != request.user:
        data = {'msg': 'this is not yours'}
        return Response(data, status=status.HTTP_403_FORBIDDEN, template_name='error_msg.html')

    if request.method == 'POST':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        # Don't worry: when Comment deleted, memo.Comment will not be cascade deleted. It is set to be None
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def like_unlike(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        try:
            LikeComment.objects.create(user=request.user, comment=comment)
        except IntegrityError:
            pass
        result = 'liked'
    elif request.method == 'DELETE':
        try:
            like = LikeComment.objects.get(user=request.user, comment=comment)
        except LikeComment.DoesNotExist:
            return Response('already liked', status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        result = 'disliked'

    return Response(result, status=status.HTTP_200_OK)
