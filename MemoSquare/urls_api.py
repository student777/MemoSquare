from django.conf.urls import url, include
from .views_api import MemoViewSet, UserViewSet, PageViewSet
from rest_framework.routers import DefaultRouter


memo_list = MemoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
memo_detail = MemoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
page_list = PageViewSet.as_view({
    'get': 'list'
})
page_detail = PageViewSet.as_view({
    'get': 'retrieve'
})

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'memo', MemoViewSet)
router.register(r'page', PageViewSet)
router.register(r'user', UserViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns=[
    url(r'', include(router.urls)),
]
