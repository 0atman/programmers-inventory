from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<username>\w{0,50})/$', views.dashboard, name='index'),
]
