from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from .models import Memo
from .serializers import MemoSerializer
from .url_classifier import classify_url
from .permissions import IsOwnerOrReadOnly


def index(request):
    return render(request, 'base.html')


def sign_out(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def sign_in(request):
    token = request.POST.get('token')
    user = authenticate(token=token)
    if user is not None:
        login(request, user)
    return HttpResponse('hello %s' % user)


def csrf_test(request):
    if request.is_ajax():
        return render(request, 'csrf_token')


# When ?format=json parameter, Hangul text is broken..
@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated, ))
def memo_list_create(request):
    is_owner = True
    if request.method == 'GET':
        query_set = Memo.objects.filter(owner__id=request.user.id)
        if query_set is not None:
            serializer = MemoSerializer(query_set, many=True)
            return Response({'memo_list': serializer.data, 'service_name': 'memo list', 'is_owner': is_owner, }, template_name='memo_list.html')

    elif request.method == 'POST':
        serializer = MemoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            page = classify_url(request.data['page'])
            serializer.save(owner=request.user, page=page)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((permissions.IsAuthenticated, ))
def memo_detail(request, pk):
    try:
        memo = Memo.objects.get(pk=pk)
    except Memo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    is_owner = memo.owner == request.user
    if request.method == 'GET':
        serializer = MemoSerializer(memo)

        try:
            memo.clipper.get(pk=request.user.pk)
            is_clipped = True
        except User.DoesNotExist:
            is_clipped = False

        num_clips = memo.clipper.count()
        owner_pic_url = memo.owner.detail.get_img_url()

        data = {}
        data['memo'] = serializer.data
        data['service_name'] = 'memo detail'
        data['is_owner'] = is_owner
        data['is_clipped'] = is_clipped
        data['num_clips'] = num_clips
        data['owner_pic_url'] = owner_pic_url

        return Response(data, template_name='memo_detail.html')

    elif request.method == 'POST':
        serializer = MemoSerializer(memo, data=request.data)
        if serializer.is_valid():
            # materialize form is fuck
            from django.utils.datastructures import MultiValueDictKeyError
            try:
                request.data['is_private']
                is_private = True
            except MultiValueDictKeyError:
                is_private = False
            serializer.save(owner=request.user, is_private=is_private)
            return Response({'memo': serializer.data}, template_name='memo_detail.html')
        return Response({'memo': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, template_name='memo_edit.html')

    elif request.method == 'DELETE':
        memo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
@permission_classes((IsOwnerOrReadOnly, ))
def memo_edit_form(request, pk):
    memo = Memo.objects.get(pk=pk)
    serializer = MemoSerializer(memo)
    return Response({'memo': serializer.data, }, template_name='memo_edit.html', )


@api_view()
@permission_classes((permissions.IsAuthenticated, ))
def memo_clipbook(request):
    is_owner = False
    query_set = Memo.objects.filter(clipper__id=request.user.id, is_private=True)
    if query_set is not None:
        serializer = MemoSerializer(query_set, many=True)
        return Response({'memo_list': serializer.data, 'service_name': 'clip book', 'is_owner': is_owner, }, template_name='memo_list.html')


@login_required()
def memo_clip(request, pk):
    memo = get_object_or_404(Memo, pk=pk)

    if request.method == 'POST':
        memo.clipper.add(request.user)
        return HttpResponse("success")

    elif request.method == 'DELETE':
        memo.clipper.remove(request.user)
        return HttpResponse("success")

    else:
        return HttpResponse("fail")


@api_view()
def memo_square(request):
    return render(request, 'square.html')


# TEST only
@api_view()
def memo_all(request):
    query_set = Memo.objects.all()
    serializer = MemoSerializer(query_set, many=True)
    return Response({'memo_list': serializer.data, 'service_name': '테스트용페이지다보인다'}, template_name='memo_list.html')
