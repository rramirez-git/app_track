from django.db import models

from app_catalogo.models import CuentaPago
from app_catalogo.models import EstatusPago
from app_cliente.models import Cliente


class Pago(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="pagos")
    concepto = models.CharField(max_length=250)
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
    fecha_de_pago = models.DateTimeField(null=True, blank=True)
    estatus = models.ForeignKey(
        EstatusPago, on_delete=models.RESTRICT, related_name="pagos")
    cuenta = models.ForeignKey(
        CuentaPago, on_delete=models.RESTRICT, related_name="pagos")

    class Meta:
        ordering = ["-estatus", "fecha_de_pago", 'pk']

    @property
    def cta(self):
        for c in CUENTAS_PAGO:
            if self.cuenta == c[0]:
                return c[1]
        return self.cuenta
