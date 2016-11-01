from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^sign_in/', views.sign_in),
    url(r'^sign_out/', views.sign_out),
    url(r'^memo/$', views.memo_list_create),
    url(r'^memo/(?P<pk>\d+)/$', views.memo_detail),
    url(r'^memo/(?P<pk>\d+)/edit/$', views.memo_edit_form),
    url(r'^memo/(?P<pk>\d+)/clip/$', views.memo_clip),
    url(r'^memo/clipbook/$', views.memo_clipbook),
    url(r'^square/', views.memo_square),
    # TEST only
    url(r'^memo/all/$', views.memo_all),
]
