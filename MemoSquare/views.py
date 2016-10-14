from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Memo, Page
from .serializers import MemoSerializer, UserSerializer, PageSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('/')


# REST framework practice
class MemoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, page=self.request.page)


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'memo': reverse('memo-list', request=request, format=format),
        'page': reverse('page-list', request=request, format=format),
    })
