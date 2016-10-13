from django.shortcuts import render, redirect
from django.contrib.auth import logout
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MemoSquare.serializers import MemoSerializer
from .models import Memo


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('/')


# REST framework practice
@api_view(['GET', 'POST'])
def memo_list(request):
    """
    List all code memos, or create a new memo.
    """
    if request.method == 'GET':
        memos = Memo.objects.all()
        serializer = MemoSerializer(memos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MemoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def memo_detail(request, pk):
    """
    Retrieve, update or delete a memo instance.
    """
    try:
        memo = Memo.objects.get(pk=pk)
    except Memo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MemoSerializer(memo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MemoSerializer(memo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        memo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
