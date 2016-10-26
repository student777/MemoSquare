from django.conf.urls import url, include
from .views_api import MemoViewSet, PageViewSet
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'memo', MemoViewSet)
router.register(r'page', PageViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns=[
    url(r'', include(router.urls)),
]
