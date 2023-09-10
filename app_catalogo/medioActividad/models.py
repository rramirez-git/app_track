from django.db import models


class MedioActividad(models.Model):
    medio = models.CharField(max_length=50)

    class Meta:
        ordering = ["medio"]

    def __str__(self):
        return self.medio.strip()

    def __unicode__(self):
        return self.__str__()
