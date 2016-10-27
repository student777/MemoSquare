from django.conf.urls import url, include
from django.contrib import admin
from . import views
from .views import MemoViewSet, PageViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'memo', MemoViewSet)
router.register(r'page', PageViewSet)


urlpatterns = [
    url(r'^$', views.index),
    url(r'^sign_in/', views.sign_in),
    url(r'^admin/', admin.site.urls),
    url(r'^sign_out/', views.sign_out),
    url(r'', include(router.urls)),
]
