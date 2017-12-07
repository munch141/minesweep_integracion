from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from builder.models import Pattern
import json

class Formulario(Pattern):
    name = 'formulario'
    form_json = JSONField(default=dict)

    def json(self):
    	return json.dumps(self.form_json, cls=DjangoJSONEncoder)

    def render(self):
        return render_to_string('patrones/formulario/view.html', {"pattern": self})

    def render_config_modal(self, request):
        return render_to_string('patrones/formulario/configurar-modal.html', {"pattern": self})

    def render_card(self):
        return render_to_string('patrones/formulario/build.html', {"pattern": self})