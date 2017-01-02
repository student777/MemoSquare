from rest_framework.decorators import permission_classes, api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from MemoSquare.models import Category
from rest_framework.renderers import JSONRenderer
from MemoSquare.serializers import CategorySerializer


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes((permissions.IsAuthenticated,))
def list_create(request):
    if request.method == 'GET':
        query_set = Category.objects.filter(owner=request.user)
        serializer = CategorySerializer(query_set, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes((permissions.IsAuthenticated,))
def detail_update_delete(request, pk):
    # get category object
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        data = {'msg': 'category does not exist'}
        return Response(data, status=status.HTTP_404_NOT_FOUND, template_name='error_msg.html')

    # permission check
    if category.owner != request.user:
        data = {'msg': 'this is not yours'}
        return Response(data, status=status.HTTP_403_FORBIDDEN, template_name='error_msg.html')

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        # Don't worry: when category deleted, memo.category will not be cascade deleted. It is set to None
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
