from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from .models import Memo
from .serializers import MemoSerializer
from .url_classifier import classify_url
from .permissions import IsOwnerOrReadOnly


def index(request):
    return render(request, 'index.html')


def sign_out(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def sign_in(request):
    # (Receive token by HTTPS POST)
    token = request.POST.get('token')
    user = authenticate(token=token)
    if user is not None:
        login(request, user)
    return HttpResponse('hello %s' % user)


# When ?format=json parameter, Hangul text is broken..
@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated, ))
def memo_list_create(request):
    if request.method == 'GET':
        query_set = Memo.objects.filter(owner__id=request.user.id)
        if query_set is not None:
            serializer = MemoSerializer(query_set, many=True)
            return Response({'memo_list': serializer.data, }, template_name='memo_list.html')

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

    if request.method == 'GET':
        serializer = MemoSerializer(memo)
        return Response(serializer.data, template_name='memo_detail.html')

    elif request.method == 'POST':
        serializer = MemoSerializer(memo, data=request.data)
        if serializer.is_valid():
            page = classify_url(request.data['page'])
            serializer.save(owner=request.user, page=page)
            return Response(serializer.data, template_name='memo_detail.html')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        memo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
@permission_classes((IsOwnerOrReadOnly, ))
def memo_edit_form(request, pk):
    memo = Memo.objects.get(pk=pk)
    serializer = MemoSerializer(memo, context={'request': request})
    return Response({'serializer': serializer, 'memo': memo, }, template_name='memo_edit.html', )


@api_view()
@permission_classes((permissions.IsAuthenticated, ))
def clipbook(request):
    query_set = Memo.objects.filter(owner__id=request.user.id)
    if query_set is not None:
        serializer = MemoSerializer(query_set, many=True)
        return Response({'memo_list': serializer.data, }, template_name='memo_clip.html')


def square(request):
    return render(request, 'square.html')
