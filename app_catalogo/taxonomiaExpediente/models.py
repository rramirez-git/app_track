from django.db import models

from app_catalogo.models import BootstrapColor


class TaxonomiaExpediente(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.ForeignKey(
        to=BootstrapColor,
        on_delete=models.RESTRICT,
        related_name="+")
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
        return f"{self.nombre.strip()}"

    def __unicode__(self):
        return self.__str__()
