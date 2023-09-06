from django.db import models

from routines.utils import BootstrapColors


class TaxonomiaExpediente(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(
        max_length=50, blank=True, choices=BootstrapColors,
        default=BootstrapColors[0][0])
    descripcion = models.TextField(
        blank=True, verbose_name="Descripción")
    mostrar_en_panel = models.BooleanField(default=False, blank=True)
    padre = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="hijos")

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return "{}".format(self.nombre).strip()

    def __unicode__(self):
        return self.__str__()
