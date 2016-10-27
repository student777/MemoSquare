from django.conf.urls import url, include
from django.contrib import admin
from . import views
from .views import MemoViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'memo', MemoViewSet)


urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^sign_in/', views.sign_in),
    url(r'^sign_out/', views.sign_out),
    url(r'^square/', views.square),
    url(r'', include(router.urls)),
]
