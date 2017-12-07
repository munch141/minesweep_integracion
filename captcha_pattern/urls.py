from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^showCaptcha/$', views.showCaptcha, name='showCaptcha'),
    url(r'^showCaptchaCode/$', views.showCaptchaCode, name='showCaptchaCode'),
    url(r'^generateCaptchaCodeZip/(?P<public_key>[a-zA-Z0-9]{1,64})/$', views.generate_captcha_code_as_zip, name='generateCaptchaCodeZip'),
    url(r'^demo/$', views.demoCaptcha, name='demoCaptcha'),

]
