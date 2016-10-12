from django.conf.urls import url, include
from django.contrib import admin
from MemoSquare import views


urlpatterns = [
    url(r'^api/', include('MemoSquare.urls-api')),
    url(r'^admin/', admin.site.urls),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^logout/', views.logout_view, name="logout"),
    url(r'^', views.index, name="index"),
]