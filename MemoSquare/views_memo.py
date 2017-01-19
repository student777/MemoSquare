from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes, api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import LimitOffsetPagination
from .models import Memo, Clip, Category, LikeMemo
from .serializers import MemoSerializer
from .finder import get_or_create_page, find_memo, get_or_create_category
from .magic import grab_img_from_content
from django.db.utils import IntegrityError


# List & Create API view
@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def list_create(request):
    # Memo list of user
    if request.method == 'GET':
        '''
        Filter memo by category
        If memo is uncategorized, category_id is 0 in request, but map as None because of query
        In short, 1: category_pk, 0: uncategorized, None: all memo
        '''
        if 'category_pk' in request.query_params:
            if request.query_params['category_pk'] is '0':
                category_pk = None
                template_title = 'uncategorized'
            else:
                category_pk = request.query_params['category_pk']
                template_title = Category.objects.get(pk=category_pk).name
            query_set = Memo.objects.filter(user=request.user, category_id=category_pk).order_by('-pk')
        # No category assigned, return all memo
        else:
            query_set = Memo.objects.filter(user=request.user).order_by('-pk')
            template_title = 'All memo'

        paginator = LimitOffsetPagination()
        paginated_query_set = paginator.paginate_queryset(query_set, request)
        serializer = MemoSerializer(paginated_query_set, many=True, context={'user': request.user})
        return Response({'memo_list': serializer.data,
                         'prev': paginator.get_previous_link(),
                         'next': paginator.get_next_link(),
                         'template_title': template_title,
                         }, template_name='memo_list.html')

    # Create Memo
    elif request.method == 'POST':
        serializer = MemoSerializer(data=request.data)
        if serializer.is_valid():
            page = get_or_create_page(request.data['page'])
            category = get_or_create_category(request.data['category_name'], request.user)
            content = grab_img_from_content(request.data['content'])
            serializer.save(user=request.user, page=page, category=category, content=content)
            return Response({'memo': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve & Update & Destory API view
@api_view(['GET', 'POST', 'DELETE'])
def detail_update_delete(request, pk):
    try:
        memo = Memo.objects.get(pk=pk)
    except Memo.DoesNotExist:
        data = {'msg': 'memo does not exist'}
        return Response(data, status=status.HTTP_404_NOT_FOUND, template_name='error_msg.html')
    '''
    Check object permissions(GET)
    Let A be a set for is_private=True, B be a set for is_owner=True
    We should kick A-B out first. ref) A-B  <-> A and ~B
    '''
    if memo.is_private and memo.user != request.user:
        data = {'msg': 'this memo is private OR you are not owner. Please log in'}
        return Response(data, status=status.HTTP_403_FORBIDDEN, template_name='error_msg.html')

    # Retrieve
    if request.method == 'GET':
        serializer = MemoSerializer(memo, context={'user': request.user})
        template_title = 'uncategorized' if memo.category is None else memo.category.name
        return Response({'memo': serializer.data, 'template_title': template_title}, template_name='memo_detail.html')

    '''
    Second check object permissions(POST, DELETE)
    We should kick ~B out, but we already kicked A-B out.
    So we should kick ~A and ~B out additionally
    '''
    if not memo.is_private and memo.user != request.user:
        data = {'msg': 'you are not an owner'}
        return Response(data, status=status.HTTP_403_FORBIDDEN, template_name='error_msg.html')

    # Update
    if request.method == 'POST':
        serializer = MemoSerializer(memo, data=request.data)
        if serializer.is_valid():
            category = get_or_create_category(request.data['category_name'], request.user)
            serializer.save(user=request.user, category=category)
            return Response({'memo': serializer.data}, template_name='memo_detail.html')
        return Response({'memo': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # Delete
    elif request.method == 'DELETE':
        memo.delete()
        # No need to redirect for web user ..?
        return Response(status=status.HTTP_204_NO_CONTENT)


# Memo list clipped by user
@api_view()
@permission_classes((permissions.IsAuthenticated,))
def clip_list(request):
    clips_by_user = Clip.objects.filter(user=request.user).order_by('-timestamp')

    # for faster response speed
    if not clips_by_user:
        return Response({'memo_list': []}, template_name='memo_list.html')

    memo_list = []
    for clip in clips_by_user:
        memo_list.append(clip.memo)

    paginator = LimitOffsetPagination()
    # It is okay that memo_list is not query_set..?
    paginated_query_set = paginator.paginate_queryset(memo_list, request)
    serializer = MemoSerializer(paginated_query_set, many=True, context={'user': request.user})

    return Response({'memo_list': serializer.data,
                     'prev': paginator.get_previous_link(),
                     'next': paginator.get_next_link(),
                     'template_title': 'clipped memo'
                     }, template_name='memo_list.html')


# Clip or Unclip a memo
@api_view(['POST', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def clip_unclip(request, pk):
    memo = get_object_or_404(Memo, pk=pk)

    # check object permissions
    if memo.is_private and memo.user != request.user:
        data = {'msg': 'this memo is private'}
        return Response(data, status=status.HTTP_403_FORBIDDEN, template_name='error_msg.html')

    # POST request: clip
    if request.method == 'POST':
        # check if there is no objects
        if Clip.objects.filter(user=request.user, memo=memo).exists():
            data = {'msg': 'there is no clip'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        clip = Clip(user=request.user, memo=memo)
        clip.save()

    # DELETE request: unclip
    elif request.method == 'DELETE':
        if Clip.objects.filter(user=request.user, memo=memo).count() == 1:
            # must return 1 object
            Clip.objects.get(user=request.user, memo=memo).delete()
        else:
            data = {'return multiple or no clip'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


@api_view()
@permission_classes((permissions.IsAuthenticated,))
def memo_square(request):
    return Response({'msg': 'Coming Soon!'}, template_name='error_msg.html')


# Memo list of an URL. If memo not exists, return None
@api_view()
@permission_classes((permissions.IsAuthenticated,))
@renderer_classes([JSONRenderer])
def find_by_page(request):
    if 'url' in request.query_params:
        page_url = request.query_params['url']
    else:
        data = 'param "url" does not exist'
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    query_set = find_memo(page_url, request)

    # for faster response speed
    if not query_set:
        return Response({'memo_list': []})

    paginator = LimitOffsetPagination()
    paginated_query_set = paginator.paginate_queryset(query_set, request)
    serializer = MemoSerializer(paginated_query_set, many=True, context={'user': request.user})
    return Response({'memo_list': serializer.data,
                     'prev': paginator.get_previous_link(),
                     'next': paginator.get_next_link(),
                     'count': len(query_set)})


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def lock_unlock(request, pk):
    memo = get_object_or_404(Memo, pk=pk)
    # check object permissions
    if memo.user != request.user:
        data = {'msg': 'you are not owner'}
        return Response(data, status=status.HTTP_403_FORBIDDEN, template_name='error_msg.html')

    # toggle boolean value
    memo.is_private = not memo.is_private
    memo.save()

    if memo.is_private:
        result = 'private'
    else:
        result = 'public'

    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def like_dislike(request, pk):
    # When Memo is None, DoesNotExist error cannot be caught in following try statement
    memo = get_object_or_404(Memo, pk=pk)

    if request.method == 'POST':
        try:
            LikeMemo.objects.create(user=request.user, memo=memo)
        except IntegrityError:
            return Response('already liked', status=status.HTTP_400_BAD_REQUEST)
        result = 'liked'
    elif request.method == 'DELETE':
        try:
            like = LikeMemo.objects.get(user=request.user, memo=memo)
        except LikeMemo.DoesNotExist:
            return Response('already disliked', status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        result = 'disliked'

    return Response(result, status=status.HTTP_200_OK)
