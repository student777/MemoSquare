from django.conf.urls import url, include
from django.contrib import admin
from . import views, urls_api


urlpatterns = [
    # TEST
    url(r'^signin/', views.sign_in),
    url(r'^signout/', views.sign_out),

    url(r'^admin/', admin.site.urls),
    url(r'^logout/', views.logout_view, name="logout"),
    url(r'^api/', include(urls_api)),
    url(r'^$', views.index, name="index"),
]
