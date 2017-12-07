from django.conf.urls import url
from .views import CarouselConfig

# Carousel URLs
urlpatterns = [
    url(
        regex='^carousel/configurar/$',
        view=CarouselConfig,
        name='carousel-config'
    ),
]
