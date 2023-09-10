from django.db import models


class FactorEdad(models.Model):
    edad = models.PositiveSmallIntegerField()
    factor_de_edad = models.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        ordering = ['edad']

    def __str__(self):
        return f"{self.edad} ({self.factor_de_edad}%)"

    def __unicode__(self):
        return self.__str__()
