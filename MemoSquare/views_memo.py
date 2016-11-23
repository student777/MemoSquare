from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes, api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import LimitOffsetPagination
from .models import Memo, Clip
from .serializers import MemoSerializer
from .classifier import classify_url, find_memo


# List & Create API view
@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated, ))
def list_create(request):
    # Memo list of user
    if request.method == 'GET':
        query_set = Memo.objects.filter(owner__id=request.user.id).order_by('-pk')

        if query_set is None:
            return Response({'memo_list': None})

        paginator = LimitOffsetPagination()
        paginated_query_set = paginator.paginate_queryset(query_set, request)
        serializer = MemoSerializer(paginated_query_set, many=True, context={'user': request.user})
        return Response({'memo_list': serializer.data, 'prev': paginator.get_previous_link(),
                         'next': paginator.get_next_link()}, template_name='memo_list.html')

    # Create Memo
    elif request.method == 'POST':
        serializer = MemoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            page = classify_url(request.data['page'])
            serializer.save(owner=request.user, page=page)
            return Response({'memo': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve & Update & Destory API view
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((permissions.IsAuthenticated, ))
def detail_update_delete(request, pk):
    try:
        memo = Memo.objects.get(pk=pk)
    except Memo.DoesNotExist:
        return HttpResponseNotFound()

    # check object permissions
    # Think about A-B  <-> A and ~B
    if memo.is_private and memo.owner != request.user:
        return HttpResponseForbidden('this memo is private OR you are not owner')

    # Retrieve
    if request.method == 'GET':
        serializer = MemoSerializer(memo, context={'user': request.user})
        return Response({'memo': serializer.data}, template_name='memo_detail.html')

    # check object permissions
    if memo.owner != request.user:
        return HttpResponseForbidden('fuck you')

    # Update
    if request.method == 'POST':
        serializer = MemoSerializer(memo, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({'memo': serializer.data}, template_name='memo_detail.html')
        return Response({'memo': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, template_name='memo_edit.html')

    # Delete
    elif request.method == 'DELETE':
        memo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Memo edit form. Same as retrieve view except for template_name, owner_pic_url
@api_view()
@permission_classes((permissions.IsAuthenticated, ))
def edit_form(request, pk):
    memo = Memo.objects.get(pk=pk)

    # check object permissions
    if memo.owner != request.user:
        return HttpResponseForbidden('fuck you')

    serializer = MemoSerializer(memo)
    return Response({'memo': serializer.data}, template_name='memo_edit.html', )


# Memo list clipped by user
@api_view()
@permission_classes((permissions.IsAuthenticated, ))
def clip_list(request):
    clips_by_user = Clip.objects.filter(user=request.user).order_by('-timestamp')

    if clips_by_user is None:
        return Response({'memo_list': None})

    memo_list = []
    for clip in clips_by_user:
        memo_list.append(clip.memo)

    paginator = LimitOffsetPagination()
    # It is okay that memo_list is not query_set..?
    paginated_query_set = paginator.paginate_queryset(memo_list, request)
    serializer = MemoSerializer(paginated_query_set, many=True, context={'user': request.user})
    return Response(
        {'memo_list': serializer.data, 'prev': paginator.get_previous_link(), 'next': paginator.get_next_link()},
        template_name='memo_list.html')


# Clip or Unclip a memo
@api_view(['POST', 'DELETE'])
@login_required()
def clip_unclip(request, pk):
    memo = get_object_or_404(Memo, pk=pk)

    # check object permissions
    if memo.is_private and memo.owner != request.user:
        return HttpResponseForbidden('this memo is private')

    # TODO: Toggle request.  POST or DELETE -> only POST. If no clip objects, create clip. Otherwise delete clip.

    # POST request: clip
    if request.method == 'POST':
        # check if there is no objects
        if Clip.objects.filter(user=request.user, memo=memo).exists():
            return HttpResponseBadRequest('there is no clip')

        clip = Clip(user=request.user, memo=memo)
        clip.save()

    # DELETE request: unclip
    elif request.method == 'DELETE':
        if Clip.objects.filter(user=request.user, memo=memo).count() == 1:
            # must return 1 object
            Clip.objects.get(user=request.user, memo=memo).delete()
        else:
            return HttpResponseBadRequest('return multiple or no clip')

    # other request: fuck you
    else:
        pass

    serializer = MemoSerializer(memo, context={'user': request.user})
    return Response({'memo':  serializer.data})


@api_view()
@permission_classes((permissions.IsAuthenticated, ))
def memo_square(request):
    query_set = Memo.objects.filter(Q(is_private=False) | Q(owner=request.user))

    if query_set is None:
        return Response({'memo_list': None})

    paginator = LimitOffsetPagination()
    paginated_query_set = paginator.paginate_queryset(query_set, request)
    serializer = MemoSerializer(paginated_query_set, many=True, context={'user': request.user})
    return Response({'memo_list': serializer.data, 'prev': paginator.get_previous_link(), 'next': paginator.get_next_link()}, template_name='memo_list.html')


# Memo list of an URL. If memo not exists, return None
@api_view()
@permission_classes((permissions.IsAuthenticated, ))
@renderer_classes([JSONRenderer])
def find_by_page(request):
    page_url = request.GET['url']
    query_set = find_memo(page_url, request)

    if query_set is None:
        return Response({'memo_list': None})

    paginator = LimitOffsetPagination()
    paginated_query_set = paginator.paginate_queryset(query_set, request)
    serializer = MemoSerializer(paginated_query_set, many=True, context={'user': request.user})
    return Response({'memo_list': serializer.data, 'prev': paginator.get_previous_link(), 'next': paginator.get_next_link()})


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def lock_unlock(request, pk):
    memo = get_object_or_404(Memo, pk=pk)
    # check object permissions
    if memo.owner != request.user:
        return HttpResponseForbidden('fuck you')

    # toggle boolean value
    memo.is_private = not memo.is_private
    memo.save()

    if memo.is_private:
        result = 'private'
    else:
        result = 'public'

    return HttpResponse(result)
