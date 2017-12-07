from django.forms import ModelForm
# from django.forms.models import inlineformset_factory
from .models import Carousel, Content

class CarouselForm(ModelForm):
    class Meta:
        model = Carousel
        fields = ['title', 'timer', 'auto', 'circular']
        labels = {
            'title': 'Título',
            'timer': 'Tiempo de transición',
            'auto': 'Transición automática',
            'circular': 'Transición circular',
        }

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'image': 'Imagen'
        }

# CarouselContentFormSet = inlineformset_factory(Carousel, Content, form=ContentForm, 
#                                                extra=2, can_delete=True)
