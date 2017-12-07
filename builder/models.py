import os
from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import camel_case_to_spaces
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

def get_user_path(username):
    return os.path.join('uploads/templates', username)

class Template(models.Model):
    # user = models.OneToOneField(User)
    # html = models.FileField(upload_to="uploads/")
    name = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def sorted_patterns(self):
        components = TemplateComponent.objects.filter(template=self).order_by('position').all()
        patterns = list(map(lambda c: c.content_object, components))
        return patterns

class TemplateComponent(models.Model):
    position = models.IntegerField(null=True)
    template = models.ForeignKey(Template, null=True)
    # Usando relaciones polimórficas de Django, relacionamos TemplateComponent
    # con patrones en particular.
    # Ref: https://simpleisbetterthancomplex.com/tutorial/2016/10/13/how-to-use-generic-relations.html
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class PatternManager(models.Manager):
    def create_pattern(self, *args, **kwargs):
        # Extraer template_id y position de los argumentos
        print(args, kwargs)
        template = kwargs.pop('template', None)
        if template:
            template_id = template.id
        elif 'template_id' in kwargs:
            template_id = kwargs.pop('template_id', None)
        position = kwargs.pop('position', 0)

        # Crear patron y asignarle un TemplateComponent
        pattern = self.model(*args, **kwargs)
        pattern.save()
        pattern.template_component.create(template_id=template_id, position=position)

        return pattern


class Pattern(models.Model):
    name = 'Nombre del patrón'
    template_component = GenericRelation(TemplateComponent, related_query_name='pattern')

    # Overriding default Manager
    objects = PatternManager()

    def template_component_id(self):
        return self.template_component.get().id

    def render(self):
        raise NotImplementedError("Debes implementar el metodo render para el patron {}".format(self))

    def render_config_modal(self, request):
        raise NotImplementedError("Debes implementar el metodo render_config_modal para el patron {}".format(self))

    def render_card(self):
        raise NotImplementedError("Debes implementar el metodo render_card para el patron {}".format(self))

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
