"""
Formularios para modelo ParametroSistema

Formularios
-----------
frmParametroSistema
    Formulario Completo
    - seccion
    - nombre
    - nombre_para_mostrar
    - tipo
"""
from zend_django.hiperforms import HorizontalModelForm

from .models import ParametroSistema


class frmParametroSistema(HorizontalModelForm):
    """
    Formulario principal del modelo ParametroSistema

    Campos
    ------
    - seccion
    - nombre
    - nombre_para_mostrar
    - tipo
    """

    class Meta:
        model = ParametroSistema
        fields = [
            'seccion',
            'nombre',
            'nombre_para_mostrar',
            'tipo',
        ]
