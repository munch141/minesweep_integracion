#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.template.loader import render_to_string
from builder.models import Pattern
import datetime


class Pregunta(Pattern):
	name = 'encuesta'

	texto_pregunta = models.CharField('Pregunta:', max_length=200)
	fecha_publ = models.DateTimeField('fecha de publicación', null=True, default=timezone.now)

	def es_reciente(self):
		return self.fecha_publ >= timezone.now() - datetime.timedelta(days=1)

	def render(self):
		return render_to_string('patrones/encuesta/view.html', {"pattern": self})

	def render_config_modal(self, request):
		return render_to_string('patrones/encuesta/configurar-modal.html', {"pattern": self})

	def render_card(self):
		return render_to_string('patrones/encuesta/build.html', {"pattern": self})

	def opciones(self):
		return self.opcion_set.all()

	def __str__(self):
		return self.texto_pregunta


class Opcion(models.Model):
	pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
	texto_opcion = models.CharField('Opción:', max_length=200)
	votos = models.IntegerField(default=0)

	def __str__(self):
		return self.texto_opcion
