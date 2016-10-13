from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Memo
from .serializers import MemoSerializer
from rest_framework import generics


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('/')


# REST framework practice
class MemoList(generics.ListCreateAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer


class MemoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
