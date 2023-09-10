from django.db import models


class EstatusPago(models.Model):
    estatus_de_pago = models.CharField(max_length=50)

    class Meta:
        ordering = ["estatus_de_pago"]

    def __str__(self):
        return self.estatus_de_pago.strip()

    def __unicode__(self):
        return self.__str__()
