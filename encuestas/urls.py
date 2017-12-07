from django.conf.urls import url

from . import views

app_name = 'encuestas'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^new/$', views.new, name='new'),
    # ex: /polls/5/
    url(r'^(?P<pregunta_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pregunta_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<pregunta_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
