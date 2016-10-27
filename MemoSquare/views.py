from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from .models import Memo, Page
from .serializers import MemoSerializer
from .url_classifier import classify_url


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


def square(request):
    return render(request, 'square.html')


class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer, )

    def perform_create(self, serializer):
        page_url = self.request.data['page']
        page_id = classify_url(page_url)
        page = Page.objects.get(pk=page_id)
        serializer.save(owner=self.request.user, page=page)

    @list_route(url_path='user')
    def get_memo_of_owner(self, request):
        memo_list = Memo.objects.filter(owner__id=request.user.id)
        if memo_list is not None:
            serializer = self.get_serializer(memo_list, many=True)
            return Response({'memo_list': serializer.data}, template_name='memo_user.html')

    # When ?format=json parameter, Hangul text is broken?
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data={'memo_list': serializer.data, }, template_name='memo_admin.html')

    @list_route(url_path='clipbook')
    def clipbook(self, request):
        memo_list = Memo.objects.filter(owner__id=request.user.id)
        if memo_list is not None:
            serializer = self.get_serializer(memo_list, many=True)
            return Response({'memo_list': serializer.data}, template_name='clipbook.html')

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
