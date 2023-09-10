from django.db import models


class EstadoCivil(models.Model):
    estado_civil = models.CharField(max_length=50)

    class Meta:
        ordering = ["estado_civil"]

    def __str__(self):
        return self.estado_civil.strip()

    def __unicode__(self):
        return self.__str__()
