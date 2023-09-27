from datetime import date
from django.contrib.auth.models import User
from django.db import models


class Alerta(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="alertas")
    nota = models.TextField()
    fecha_alerta = models.DateField(default=date.today)
    alertado = models.BooleanField(default=False)
    fecha_alertado = models.DateField(null=True, blank=True)
    mostrar_alerta = models.BooleanField(default=True)
    fecha_no_mostrar = models.DateField(null=True, blank=True)
    creado_por = models.TextField(max_length=250, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizado_por = models.TextField(max_length=250, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_alerta", "-actualizado_por", "-creado_por"]
        permissions = [
            ('get_alerta', 'Obtener mis alertas'),
            ('disabled_alerta', 'Desactivar alerta'),
        ]

    def __str__(self) -> str:
        return f"{self.fecha_alerta}: {self.nota}"
