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
    url(r'^memo/$', views.MemoList.as_view()),
    url(r'^memo/(?P<pk>[0-9]+)/$', views.MemoDetail.as_view()),
    url(r'^', views.index, name="index"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
