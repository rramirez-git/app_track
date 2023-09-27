from django.contrib.auth.models import User
from django.db import models


class Nota(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notas")
    nota = models.TextField()
    creado_por = models.TextField(max_length=250, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizado_por = models.TextField(max_length=250, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_creacion", "-fecha_actualizacion"]

    def __str__(self) -> str:
        return f"{self.nota}"
