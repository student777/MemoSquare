from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^sign_in/', views.sign_in),
    url(r'^sign_out/', views.sign_out),
    url(r'^square/', views.square),
    url(r'^memo/clipbook/$', views.MemoViewSet.as_view({'get': 'clipbook'})),
    url(r'^memo/$', views.MemoViewSet.as_view({'get': 'list'})),
    url(r'^memo/user/$', views.MemoViewSet.as_view({'get': 'get_memo_of_owner'})),
    url(r'^memo/(?P<pk>[^/.]+)/$', views.MemoViewSet.as_view({'get': 'retrieve', 'post': 'update'})),
    url(r'^memo/(?P<pk>[^/.]+)/edit/$', views.MemoViewSet.as_view({'get': 'edit', })),
]
