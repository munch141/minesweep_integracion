#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.template.loader import render_to_string
from builder.models import Pattern
from django import forms
import datetime

class Faq(Pattern):
    name = 'faq'
    
    fecha_creacion = models.DateTimeField('fecha de creacion:', null=True, default=timezone.now)

    def es_reciente(self):
        return self.fecha_publ >= timezone.now() - datetime.timedelta(days=1)

    def preguntas(self):
        return PreguntaFaq.objects.filter(faq=self).order_by('id').all()

    def categoria(self):
        return Categoria.objects.get(faq=self)

    def render(self):
        return render_to_string('patrones/faqs/view.html', {"pattern": self})

    def render_card(self):
        return render_to_string('patrones/faqs/build.html', {"pattern": self})

    def render_config_modal(self, request):
        return render_to_string('patrones/faqs/configurar-formulario.html', {"pattern": self})

    def __str__(self):
        return self.name

class Categoria(models.Model):
    faq = models.ForeignKey(Faq, on_delete=models.CASCADE, null=True)
    nombre = models.CharField('Tema:', max_length=100, blank=True)
    fecha_publ = models.DateTimeField('fecha de creacion:', null=True, default=timezone.now)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class PreguntaFaq(models.Model):
    faq = models.ForeignKey(Faq, on_delete=models.CASCADE, null=True)
    tema = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    pregunta = models.CharField('Pregunta:', max_length=100, blank=False)
    respuesta = models.TextField('Respuesta:', max_length=250, blank=False)

    class Meta:
            ordering = ["id"]

    def __str__(self):
        return self.pregunta
