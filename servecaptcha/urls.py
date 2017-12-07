from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name = 'servecaptcha'

urlpatterns = [
    url(r'^captcha\.js$', views.captcha_js, name="captcha_js"),
    url(r'^image/(?P<captcha_id>[a-zA-Z0-9]{64})?$', views.serve_captcha_image),
    url(r'^audio/(?P<captcha_id>[a-zA-Z0-9]{64})?$', views.serve_captcha_audio),
    url(r'^generate_apikey/$', views.generate_apikey, name="generate_apikey"),
    url(r'^generate_captcha/(?P<public_key>[a-zA-Z0-9]{1,64})/$', views.generate_captcha, name="generate_captcha"),
    url(r'^validate_captcha/$', views.validate_captcha, name="validate_captcha"),
    url(r'^$', views.api_documentation, name="captcha_api_documentation"),

]
