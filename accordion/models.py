# -*- coding: utf-8 -*-
import uuid
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from builder.models import Pattern, PatternManager


class BaseAccordionManager(PatternManager):
    def get_queryset(self):
        return super(BaseAccordionManager, self).get_queryset().filter(parent=None).order_by('id')


class PatronAbstract(models.Model):
    """docstring for ClassName"""
    content = models.TextField(
        u'Contenido',
        blank=True,
        null=True
    )
    content_color = models.CharField(
        u'Color del contenido',
        max_length=50,
        blank=True,
        null=True
    )
    content_style = models.TextField(
        u'Estilos del contenido',
        blank=True,
        null=True
    )
    border_style = models.TextField(
        u'Definir tipo de borde',
        blank=True,
        null=True
    )
    border_color = models.CharField(
        u'Color del borde',
        max_length=50,
        blank=True,
        null=True
    )
    border_radius = models.CharField(
        u'Radio del borde (px)',
        max_length=50,
        blank=True,
        null=True,
        default='0'
    )
    width = models.CharField(
        u'Ancho (%)',
        max_length=50,
        blank=True,
        null=True,
        default='100'
    )
    height = models.CharField(
        u'Alto (px)',
        max_length=50,
        blank=True,
        null=True,
        default='30'
    )
    style = models.TextField(
        u'Extra CSS',
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    def toHtml(self, template_name, var_name):
        return render_to_string(template_name, context={
            var_name: self,
        }
    )


class Accordion(PatronAbstract, Pattern):
    name = 'accordion'

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='panels'
    )
    accordion_id = models.UUIDField(
        u'Id del acordeon',
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(
        u'Título',
        max_length=50
    )
    title_style = models.TextField(
        u'Estilos del Título',
        blank=True,
        null=True
    )    

    # objects returns accordions that have no parent.
    # all_objects returns all accordions, with out without parents.
    objects = BaseAccordionManager()
    all_objects = models.Manager()

    def __str__(self):
        return str(self.id)

    def get_uuid_as_str(self):
        return str(self.accordion_id)

    def get_child_panels(self):
        panels = Accordion.all_objects.filter(parent=self.id).order_by('id')
        return panels

    def render(self):
        # return render_to_string('patrones/accordion/view.html', {"pattern": self})
        return "UUUUUUUUUUUYUYUYUYUYY"

    def render_card(self):
        # return render_to_string('patrones/accordion/build.html', {"pattern": self})
        return "HUEHUEHUEHUEHUEHUEHEUH"

    def render_config_modal(self, request):
        from .forms import AccordionForm
        form = AccordionForm()

        return render_to_string('patrones/accordion/configurar-modal.html', {"accordionForm": form})

