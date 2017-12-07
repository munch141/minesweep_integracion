from django.conf.urls import url
from .views import *

# Pagination URLs
urlpatterns = [
    url(
        regex='^pagination/configurar/$',
        view=pagination_config,
        name='pagination-config'
    ),
    url(
        regex='^pagination/configurar/(?P<pk>[0-9]+)$',
        view=pagination_update,
        name='pagination-modify'
    ),
    url(
        regex='^pagination/eliminar/$',
        view=pagination_delete,
        name='pagination-delete'
    ),
]
