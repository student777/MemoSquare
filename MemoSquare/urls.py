from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^sign_in/', views.sign_in),
    url(r'^sign_out/', views.sign_out),
    url(r'^square/', views.square),
    url(r'^memo/$', views.create_memo),
    url(r'^memo/all/$', views.all_memo),
    url(r'^memo/clipbook/$', views.clipbook),
    url(r'^memo/user/$', views.my_memo),
    url(r'^memo/(?P<pk>[^/.]+)/$', views.detail_memo),
    url(r'^memo/(?P<pk>[^/.]+)/edit/$', views.edit_memo),
]