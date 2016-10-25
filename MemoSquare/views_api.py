from .models import Memo, Page
from .serializers import MemoSerializer, UserSerializer, PageSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly


class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    class Meta:
        model = Memo
        fields = ('url', 'pk', 'content', 'owner', 'page',
                  'clipper', 'is_private', 'timestamp')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, page=self.request.page)

    @list_route(url_path='user')
    def get_memo_of_owner(self, request):
        memo_list = Memo.objects.filter(owner__id=request.user.id)
        if memo_list is not None:
            serializer = self.get_serializer(memo_list, many=True)
            return Response(serializer.data)


class PageViewSet(viewsets.ReadOnlyModelViewSet):
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