from django.contrib import admin
from .models import Carousel, Content

class ContentInline(admin.TabularInline):
    model = Content

class CarouselAdmin(admin.ModelAdmin):
    inlines = [ContentInline, ]

admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Content)
