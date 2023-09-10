from app_catalogo.models import BootstrapColor
from django.db import models


class EstatusActividad(models.Model):
    estatus_de_la_actividad = models.CharField(max_length=50)
    color = models.ForeignKey(
        to=BootstrapColor,
        on_delete=models.RESTRICT,
        related_name="+")
    mostrar_en_panel = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ["estatus_de_la_actividad"]

    def __str__(self):
        return self.estatus_de_la_actividad.strip()

    def __unicode__(self):
        return self.__str__()
