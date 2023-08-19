"""
Formularios para modelo ParametroUsuario

Formularios
-----------
frmParametroUsuario
    Formulario Completo
    - seccion
    - nombre
    - valor_default
    - tipo
"""

from .models import ParametroUsuario
from zend_django.hiperforms import HorizontalModelForm


class frmParametroUsuario(HorizontalModelForm):
    """
    Formulario principal del modelo ParametroUsuario

    Campos
    ------
    - seccion
    - nombre
    - valor_default
    - tipo
    """

    class Meta:
        model = ParametroUsuario
        fields = [
            'seccion',
            'nombre',
            'valor_default',
            'tipo',
        ]
