from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import Http404
from .models import Memo
from .serializers import MemoSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('/')


# REST framework practice
class MemoList(APIView):
    """
    List all memos, or create a new memo.
    """
    def get(self, request, format=None):
        memos = Memo.objects.all()
        serializer = MemoSerializer(memos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MemoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemoDetail(APIView):
    """
    Retrieve, update or delete a memo instance.
    """
    def get_object(self, pk):
        try:
            return Memo.objects.get(pk=pk)
        except Memo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        memo = self.get_object(pk)
        serializer = MemoSerializer(memo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        memo = self.get_object(pk)
        serializer = MemoSerializer(memo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        memo = self.get_object(pk)
        memo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
