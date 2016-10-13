from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Memo
from .serializers import MemoSerializer, UserSerializer
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('/')


# REST framework practice
class MemoList(generics.ListCreateAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MemoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
