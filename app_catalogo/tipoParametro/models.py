"""
Definición de modelos de Tipos de Parámetros

Modelos
-------
- TipoParametro
"""
from django.db import models

class TipoParametro(models.Model):
    """
    Modelo de Tipos de paramétro
    """
    nombre = models.CharField(max_length=100, unique=True)
    tipo_interno = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nombre']
        unique_together = [
            ['nombre', 'tipo_interno']
        ]

    def __str__(self) -> str:
        return self.nombre.strip()
    
    def __unicode__(self) -> str:
        return self.__str__()
    