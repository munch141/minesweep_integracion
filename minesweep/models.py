import uuid
from django.db import models
from django.template.loader import render_to_string

from accordion.models import PatronAbstract
from builder.models import Pattern, PatternManager

class BaseMinesweepManager(PatternManager):
    def get_queryset(self):
        return super(BaseMinesweepManager, self).get_queryset().filter(parent=None).order_by('id')


class Minesweep(PatronAbstract, Pattern):
    name = 'minesweep'

    SIDE_CHOICES = (
        ('top', 'arriba'),
        ('bottom', 'abajo'),
        ('right', 'derecha'),
        ('left', 'izquierda'),
    )

    tooltip_side = models.CharField(
        u'Lado del tootlip',
        max_length=6,
        choices=SIDE_CHOICES,
        default='arriba'
    )
    minesweep_id = models.UUIDField(
        u'Id del minesweep',
        default=uuid.uuid4,
        editable=False
    )
    tooltip = models.TextField(
        u'Información del tooltip',
        blank=True,
        null=True
    )
    tooltip_style = models.TextField(
        u'Estilos del tooltip',
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.id)

    def get_uuid_as_str(self):
        return str(self.minesweep_id)


    def render(self):
        # return render_to_string('patrones/minesweep/view.html', {"pattern": self})
        return "UUUUUUUUUUUYUYUYUYUYY"

    def render_card(self):
        # return render_to_string('patrones/minesweep/build.html', {"pattern": self})
        return "HUEHUEHUEHUEHUEHUEHEUH"

    def render_config_modal(self, request):
        from .forms import MinesweepForm
        form = MinesweepForm()

        return render_to_string('patrones/minesweep/configurar-modal.html', {"minesweepForm": form})
