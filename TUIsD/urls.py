"""TUIsD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.contrib import admin
from django.conf.urls import url
from builder.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^faqs/', include('faqs.urls')),
    url(r'^encuestas/', include('encuestas.urls', namespace='encuestas')),
    url(r'^builder/', include('builder.urls')),
    url(r'^acordeon/', include('accordion.urls', namespace='accordion')),
    url(r'^', include('carrusel.urls')),
    url(r'^pagination/', include('pagination.urls')),
    url(r'^$', homeTemplate.as_view(), name = 'home'),
    url(r'^ver_templates/', ver_templatesTemplate.as_view(), name = 'ver_templates'),
    url(r'^revisar_template/(?P<templateID>[0-9]+)$',revisarTemplate.as_view(), name='revisar'),
    url(r'^crear_usuario/', userTemplate.as_view(), name = 'crear_usuario'),
    url(r'^login/', loginTemplate.as_view(), name = 'login'),
    url(r'^logout/', logout_view , name = 'logout'),
    url(r'^servecaptcha/', include('servecaptcha.urls'))
]

# JSWeCan patterns and services.
# urlpatterns += [
#     url(r'^servecaptcha/', include('servecaptcha.urls'))
# ]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
