from datetime import date
from django.db import models


def getyear():
    return date.today().year


class UMA(models.Model):
    año = models.PositiveSmallIntegerField(default=getyear, unique=True)
    valor = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["-año"]

    def __str__(self):
        return str(self.año)

    def __unicode__(self):
        return self.__str__()

    @staticmethod
    def max():
        try:
            return UMA.objects.all()[0].pk
        except IndexError:
            return 0
