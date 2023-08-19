"""
Formularios para modelo Favorito

Formularios
-----------
frmFavorito
    Formulario Completo
    - usuario
    - url
    - etiqueta
"""
from django import forms

from .models import Favorito
from zend_django.hiperforms import HorizontalModelForm


class frmFavorito(HorizontalModelForm):
    """
    Formulario principal del modelo Favorito

    Campos
    ------
    - usuario
    - url
    - etiqueta
    """

    class Meta:
        model = Favorito
        fields = [
            'usuario',
            'etiqueta',
            'url',
        ]
