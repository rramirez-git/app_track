from django.db import models


class CuentaPago(models.Model):
    cuenta_de_pago = models.CharField(max_length=50)

    class Meta:
        ordering = ["cuenta_de_pago"]

    def __str__(self):
        return self.cuenta_de_pago.strip()

    def __unicode__(self):
        return self.__str__()
