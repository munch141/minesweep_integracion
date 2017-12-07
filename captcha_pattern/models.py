from django.db import models
from django.contrib.postgres.fields import JSONField
from django.template.loader import render_to_string
from builder.models import Pattern
from servecaptcha.models import KeyPair
from servecaptcha.utils import random_string

class Captcha(Pattern):
    name = 'captcha'
    public_key = models.CharField(max_length=64, default=random_string.alphanumeric, unique=True)
    private_key = models.CharField(max_length=64, default=random_string.alphanumeric, unique=True)

    def render(self):
	    return render_to_string('patrones/captcha_pattern/view.html', {"pattern": self})

    def render_card(self):
	    return render_to_string('patrones/captcha_pattern/build.html', {"pattern": self})

    def render_config_modal(self, request):
	    return render_to_string('patrones/captcha_pattern/configurar-modal.html', {"pattern": self})

    def __str__(self):
	    return "Captcha"
