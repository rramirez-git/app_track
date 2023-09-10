from django.db import models


class BootstrapColor(models.Model):
    nombre = models.CharField(max_length=50)
    clase_color = models.CharField(max_length=50)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.clase_color.strip()

    def __unicode__(self):
        return self.__str__()
