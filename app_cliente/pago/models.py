from django.db import models

from app_cliente.models import Cliente


STATUS_PAGO = (
    ('pendiente', 'Pendiente de Pago'),
    ('pagado', 'Pagado'),
    ('verificado', 'Pagado y Verificado')
)


CUENTAS_PAGO = (
    ('efectivo', 'Efectivo'),
    ('daniel azteca', 'Daniel Azteca'),
    ('daniel banamex', 'Daniel Banamex'),
    ('sosa del bosque', 'Sosa del Bosque'),
)


class Pago(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="pagos")
    concepto = models.CharField(max_length=250)
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
    fecha_de_pago = models.DateTimeField(null=True, blank=True)
    estatus = models.CharField(
        max_length=20, choices=STATUS_PAGO, default='pendiente')
    cuenta = models.CharField(
        max_length=50, blank=True, choices=CUENTAS_PAGO, default='efectivo')

    class Meta:
        ordering = ["-estatus", "fecha_de_pago", 'pk']

    @property
    def cta(self):
        for c in CUENTAS_PAGO:
            if self.cuenta == c[0]:
                return c[1]
        return self.cuenta
