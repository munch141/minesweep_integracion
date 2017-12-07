from django.db import models
from django.core.validators import MinValueValidator
from builder.models import Pattern
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.forms import inlineformset_factory


class Carousel(Pattern):
    name = 'carousel'

    title = models.CharField(max_length=50)
    timer = models.IntegerField(
        blank=True, default=3, validators=[MinValueValidator(0)])
    auto = models.BooleanField(default=False)
    circular = models.BooleanField(default=True)

    def render(self):
        return render_to_string('patrones/carrusel/view.html', {"pattern": self})

    def render_config_modal(self, request):
        return rendering_form(self, request)

    def render_card(self):
        return render_to_string('patrones/carrusel/build.html', {"pattern": self})

    def __str__(self):
        return self.name + ": " + str(self.pk) + "; title:" + self.title + "; timer: " + str(self.timer)


class Content(models.Model):
    carousel = models.ForeignKey(Carousel, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=256, blank=True)
    image = models.ImageField(upload_to='carouselImages/')

    def __str__(self):
        return self.title

def rendering_form(carousel, request):
    from .forms import CarouselForm

    ContentInlineFormSet = inlineformset_factory(
        Carousel, Content, fields=('title', 'description', 'image'), extra=2
    )
    form = CarouselForm(instance=carousel)
    formset = ContentInlineFormSet(instance=carousel)
    return render_to_string(
        template_name='carrusel/configurar-modal.html',
        context={'formset': formset, 'form': form, 'carousel': carousel},
        request=request
    )
