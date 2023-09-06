from django.db import models

from app_cliente.models import Cliente


class Acuerdo(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="acuerdos")
    titulo = models.CharField(max_length=250)
    acuerdo = models.TextField()
    aceptado = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(
        null=True, verbose_name="IP de aceptación")
    fechaHora = models.DateTimeField(
        null=True, verbose_name="Fecha de Aceptación")

    class Meta:
        ordering = ["titulo", 'aceptado', 'fechaHora']

    @property
    def acuerdoStr(self):
        return "\n".join([f"<p>{p}</p>" for p in self.acuerdo.split('\n')])

    def __str__(self):
        return f"<h3>{self.titulo}</h3>{self.acuerdoStr}"
