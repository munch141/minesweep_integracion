from django import forms
from .models import *
from django.forms.formsets import BaseFormSet
from django.forms import inlineformset_factory
from django.forms.formsets import formset_factory

class CategoriaForm(forms.ModelForm):
    class Meta: 
        model = Categoria
        fields = ['nombre']

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = PreguntaFaq
        fields = ['pregunta', 'respuesta']
        widgets = {
          'respuesta': forms.Textarea(attrs={'rows':4}),
        }