"""
Funciones de apoyo para la obtención e inclusion de parámetros del sistema
dentro de templates HMTL.

Cargar con {% load parametros_helpers %}
"""

from django import template
from django.utils.safestring import mark_safe
from zend_django.parametrosistema.models import ParametroSistema
from zend_django.parametrousuario.models import ParametroUsuarioValor
from zend_django.parametrosistema.models import parametro_upload_to

register = template.Library()


@register.simple_tag
def parametro_de_sistema(seccion, nombre):
    """
    Devuelve el valor establecido para un parámetro de sistema

    Parameters
    ----------
    seccion : string
        Seccion con la que se almacena del parámetro
    nombre : string
        Nombre del parámetro

    Returns
    -------
    string
        valor almacenado para el parámetro, la cadena es una cadena segura

    Raises
    ------
    ParametroSistema.DoesNotExist
        No existe una combinacion entre la seccion y el nombre enviados
    """
    return mark_safe(ParametroSistema.get(seccion, nombre))


@register.simple_tag
def parametro_de_usuario(seccion, nombre, username):
    return mark_safe(ParametroUsuarioValor.get(seccion, nombre, username))
