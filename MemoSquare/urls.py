from django.conf.urls import url, include
from django.contrib import admin
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^logout/', views.logout_view, name="logout"),
    # REST practice
    # url(r'^api/', include('MemoSquare.urls-api')),
    url(r'^memo/$', views.MemoList.as_view(), name='memo-list'),
    url(r'^memo/(?P<pk>[0-9]+)/$', views.MemoDetail.as_view(), name='memo-detail'),
    url(r'^user/$', views.UserList.as_view(), name='user-list'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^page/$', views.PageList.as_view(), name='page-list'),
    url(r'^page/(?P<pk>[0-9]+)/$', views.PageDetail.as_view(), name='page-detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.api_root),
    # url(r'^', views.index, name="index"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
