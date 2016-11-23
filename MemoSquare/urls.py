from django.conf.urls import url
from django.contrib import admin
from . import views, views_memo


urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^sign_in/', views.sign_in),
    url(r'^sign_out/', views.sign_out),
    url(r'^memo/$', views_memo.list_create),
    url(r'^memo/page/$', views_memo.find_by_page),
    url(r'^memo/clipbook/$', views_memo.clip_list),
    url(r'^memo/(?P<pk>\d+)/$', views_memo.detail_update_delete),
    url(r'^memo/(?P<pk>\d+)/edit/$', views_memo.edit_form),
    url(r'^memo/(?P<pk>\d+)/clip/$', views_memo.clip_unclip),
    url(r'^memo/(?P<pk>\d+)/lock/$', views_memo.lock_unlock),
    url(r'^square/', views_memo.memo_square),
    # TEST only
    url(r'^memo/csrf_test/$', views.csrf_test),
]
