from django.db import models


class TipoActividad(models.Model):
    tipo_de_actividad = models.CharField(max_length=50)

    class Meta:
        ordering = ["tipo_de_actividad"]

    def __str__(self):
        return self.tipo_de_actividad.strip()

    def __unicode__(self):
        return self.__str__()
