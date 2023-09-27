"""
Definición de modelos de Parámetros

Modelos
-------
- ParametroSistema      => Parámetros de sistema

Constantes
----------
- parametro_upload_to
"""
from app_catalogo.models import TipoParametro
from django.db import models

testing = True

parametro_upload_to = "parametrosistema"


class ParametroSistema(models.Model):
    """
    Modelo de Parámetros del Sistema
    """
    seccion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    nombre_para_mostrar = models.CharField(max_length=100)
    valor = models.TextField()
    tipo = models.ForeignKey(
        to=TipoParametro,
        on_delete=models.RESTRICT,
        related_name="+")
    es_multiple = models.BooleanField(default=False)

    class Meta:
        ordering = ['seccion', 'nombre_para_mostrar']
        unique_together = ['seccion', 'nombre']

    def __str__(self):
        if self.valor:
            return "{}: {}".format(self.nombre_para_mostrar, self.valor)
        return self.nombre_para_mostrar

    @property
    def tipo_txt(self):
        """
        Tipo de parámetro, version para mostrar
        """
        return f"{self.tipo}"

    @staticmethod
    def get(seccion, nombre):
        """
        Obtiene el valor del parámetro

        Parameters
        ----------
        seccion : string
            Seccion del parámetro

        nombre : string
            Nombre del parámetro

        Returns
        -------
        string
            Valor del parámetro o "Parámetro se Sistema no encontrado" en
            caso de que no exista el parametro solicitado
        """
        try:
            return ParametroSistema.objects.get(
                seccion=seccion, nombre=nombre).valor
        except ParametroSistema.DoesNotExist:
            return f"Parámetro de Sistema no encontrado: {seccion} / {nombre}"
