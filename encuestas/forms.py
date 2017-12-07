from django import forms
from .models import *
from django.forms.formsets import BaseFormSet
from django.forms import inlineformset_factory
from django.forms.formsets import formset_factory

class PreguntaForm(forms.ModelForm):
    class Meta: 
        model = Pregunta
        fields = ['texto_pregunta']

class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ['texto_opcion']