from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import permission_classes, api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import Memo
from .serializers import MemoSerializer
from .classifier import classify_url, find_memo


def index(request):
    return render(request, 'base.html')


# Facebook oauth2 token login
@csrf_exempt
def sign_in(request):
    token = request.POST.get('token')
    user = authenticate(token=token)
    if user is not None:
        login(request, user)
    return HttpResponse('hello %s' % user)


def sign_out(request):
    logout(request)
    return redirect('/')


# List & Create API view
@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated, ))
def memo_list_create(request):
    # Memo list of user
    if request.method == 'GET':
        query_set = Memo.objects.filter(owner__id=request.user.id)

        if query_set is not None:
            serializer = MemoSerializer(query_set, many=True, context={'user': request.user})
            return Response({'memo_list': serializer.data}, template_name='memo_list.html')

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
def memo_detail(request, pk):
    try:
        memo = Memo.objects.get(pk=pk)
    except Memo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # check object permissions
    if memo.is_private:
        return HttpResponseForbidden('this memo is private')

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
def memo_edit_form(request, pk):
    memo = Memo.objects.get(pk=pk)

    # check object permissions
    if memo.owner != request.user:
        return HttpResponseForbidden('fuck you')

    serializer = MemoSerializer(memo)
    return Response({'memo': serializer.data}, template_name='memo_edit.html', )


# Memo list clipped by user
@api_view()
@permission_classes((permissions.IsAuthenticated, ))
def memo_clipbook(request):
    query_set = Memo.objects.filter(clipper__id=request.user.id)
    if query_set is not None:
        serializer = MemoSerializer(query_set, many=True, context={'user': request.user})
        return Response({'memo_list': serializer.data}, template_name='memo_list.html')


# Clip or Unclip a memo
@api_view(['POST', 'DELETE'])
@login_required()
def memo_clip(request, pk):
    memo = get_object_or_404(Memo, pk=pk)

    # check object permissions
    if memo.is_private and memo.owner != request.user:
        return HttpResponseForbidden('this memo is private')

    # POST request: clip
    if request.method == 'POST':
        memo.clipper.add(request.user)

    # DELETE request: unclip
    elif request.method == 'DELETE':
        memo.clipper.remove(request.user)

    # other request: fuck you
    else:
        pass

    serializer = MemoSerializer(memo, context={'user': request.user})
    return Response({'memo':  serializer.data})


def memo_square(request):
    return render(request, 'square.html')


# Memo list of an URL. If memo not exists, return None
@api_view()
@renderer_classes([JSONRenderer])
def memo_page(request):
    page_url = request.GET['url']
    query_set = find_memo(page_url)
    serializer = MemoSerializer(query_set, many=True, context={'user': request.user})
    return Response({'memo_list': serializer.data})


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def memo_lock(request, pk):
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


# TEST only
@api_view()
def memo_all(request):
    query_set = Memo.objects.all()
    serializer = MemoSerializer(query_set, many=True, context={'user': request.user})
    return Response({'memo_list': serializer.data}, template_name='memo_list.html')


# TEST? For cross browsing request(chrome extension)
def csrf_test(request):
    if request.is_ajax():
        return render(request, 'csrf_token')

