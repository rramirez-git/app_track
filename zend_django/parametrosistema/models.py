"""
Definición de modelos de Parámetros

Modelos
-------
- ParametroSistema      => Parámetros de sistema

Constantes
----------
- PARAM_TYPES
- PARAM_TYPES_Tuples
- parametro_upload_to
"""
from django.contrib.auth.models import User
from django.db import models

testing = True

parametro_upload_to = "parametrosistema"

PARAM_TYPES = {
    'ENTERO': 'INTEGER',
    'CADENA': 'STRING',
    'TEXTO_LARGO': 'TEXT',
    'IMAGEN': 'PICTURE',
    'ARCHIVO': 'FILE',
    'DECIMAL': 'DECIMAL',
}

PARAM_TYPES_Tuples = (
        (PARAM_TYPES['ENTERO'], 'Entero'),
        (PARAM_TYPES['CADENA'], 'Cadena'),
        (PARAM_TYPES['TEXTO_LARGO'], 'Texto Largo'),
        (PARAM_TYPES['IMAGEN'], 'Imagen'),
        (PARAM_TYPES['ARCHIVO'], 'Archivo'),
        (PARAM_TYPES['DECIMAL'], 'Decimal'),
    )


def get_param_type_to_show(type):
    """
    Obtiene el valor para mostrar de un tipo de parámetro

    Parameters
    ----------
    type : string
        Tipo de parámetro [ENTERO, CADENA, TEXTO_LARGO, IMAGEN, ARCHIVO]

    Returns
    -------
    string
        Valor para mostrar del tipo de parámetro
    """
    for param in PARAM_TYPES_Tuples:
        if param[0] == type:
            return param[1]
    return ""


class ParametroSistema(models.Model):
    """
    Modelo de Parámetros del Sistema
    """
    seccion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    nombre_para_mostrar = models.CharField(max_length=100)
    valor = models.TextField()
    tipo = models.CharField(
        max_length=20, choices=PARAM_TYPES_Tuples,
        default=PARAM_TYPES['CADENA'])
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
        return get_param_type_to_show(self.tipo)

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

