from .models import Memo, Page
from .serializers import MemoSerializer, PageSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, list_route, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .url_classifier import *


class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer

    def perform_create(self, serializer):
        page_url = self.request.data['page']
        page_id = classify_url(page_url)
        page = Page.objects.get(pk=page_id)
        serializer.save(owner=self.request.user, page=page)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @list_route(url_path='user')
    def get_memo_of_owner(self, request):
        memo_list = Memo.objects.filter(owner__id=request.user.id)
        if memo_list is not None:
            serializer = self.get_serializer(memo_list, many=True)
            return Response(serializer.data)

    # This is stupid function because DRF.decorator permission not working
    # ref)http://stackoverflow.com/questions/25283797/django-rest-framework-add-additional-permission-in-viewset-update-method
    def get_permissions(self):
        if self.request.path.endswith('/user/'):
            self.permission_classes = [permissions.IsAuthenticated, ]
        elif self.request.path.endswith('/memo/'):
            self.permission_classes = [permissions.IsAdminUser, ]
        else:
            self.permission_classes = [permissions.IsAuthenticated, ]
        return super(MemoViewSet, self).get_permissions()


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'memo': reverse('memo-list', request=request, format=format),
        'page': reverse('page-list', request=request, format=format),
    })