from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from builder.views import *
from . import views

urlpatterns = [
    url(r'^build/(?P<templateID>[0-9]+)$', editarTemplate.as_view(), name='editar'),
    url(r'^build/$', buildTemplate.as_view(), name='build'),
    url(r'^poll-config/$', views.pollConfig, name='pollConfig'),
    url(r'^faq-config/$', views.faqConfig, name='faqConfig'),
    url(r'^form-config/$', views.formConfig, name='formConfig'),
    url(r'^accordion-config/$', views.accordionConfig, name='accordionConfig'),
    url(r'^minesweep-config/$', views.minesweepConfig, name='minesweepConfig'),
    url(r'^captcha-config/$', views.captchaConfig, name='captchaConfig'),
    url(r'^erase-captcha/$', views.eraseCaptcha, name='eraseCaptcha'),
    url(r'^new-template/$', views.newTemplate, name='newTemplate'),
    url(r'^erase-question/$', views.eraseQuestion, name='eraseQuestion'),
    url(r'^create-poll/$', views.createPoll, name='createPoll'),
    url(r'^captcha/', include('captcha_pattern.urls')),
    url(r'^config-modal/$', views.configModal, name='configModal'),
    url(r'^delete-pattern/$', views.deletePattern, name='deletePattern'),
    url(r'^navbar-config/$', views.navbarConfig, name='navbarConfig'),
]
