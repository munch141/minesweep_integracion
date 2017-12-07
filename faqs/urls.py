from django.conf.urls import url

from . import views

app_name = 'faqs'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^new/$', views.new, name='new'),
    # ex: /polls/5/
    url(r'^detail/$', views.detail, name='detail'),
    # ex: /polls/5/results/

]
