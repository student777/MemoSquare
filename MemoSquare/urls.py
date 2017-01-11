from django.conf.urls import url
from django.contrib import admin
from . import views, views_memo, views_category
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^sign_in/', views.sign_in),
    url(r'^sign_out/', views.sign_out),
    url(r'^report/', views.report),
    url(r'^upload/$', views.upload),
    url(r'^memo/$', views_memo.list_create),
    url(r'^memo/page/$', views_memo.find_by_page),
    url(r'^memo/clipbook/$', views_memo.clip_list),
    url(r'^memo/(?P<pk>\d+)/$', views_memo.detail_update_delete),
    url(r'^memo/(?P<pk>\d+)/clip/$', views_memo.clip_unclip),
    url(r'^memo/(?P<pk>\d+)/lock/$', views_memo.lock_unlock),
    url(r'^square/', views_memo.memo_square),
    url(r'^category/$', views_category.list_create),
    url(r'^category/(?P<pk>\d+)/$', views_category.detail_update_delete),
    # TEST only
    url(r'^memo/csrf_test/$', views.csrf_test),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)