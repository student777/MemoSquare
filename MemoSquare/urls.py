from django.conf.urls import url, include
from django.contrib import admin
from . import views, urls_api


urlpatterns = [
    url(r'^sign_in/', views.sign_in),
    url(r'^admin/', admin.site.urls),
    url(r'^sign_out/', views.sign_out),
    url(r'^api/', include(urls_api)),
    url(r'^$', views.index),
]
