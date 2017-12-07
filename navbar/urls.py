from django.conf.urls import url

from . import views

app_name = 'navbar'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^showCodigo/$', views.showCodigo, name='showCodigo')
]
