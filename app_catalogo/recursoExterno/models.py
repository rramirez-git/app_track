from django.db import models


class RecursoExterno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100, blank=True)
    apellido_materno = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["nombre", 'apellido_paterno', 'apellido_materno']

    def __str__(self):
        return f"{self.nombre.strip()} {self.apellido_paterno.strip()} {self.apellido_materno.strip()}"

    def __unicode__(self):
        return self.__str__()
