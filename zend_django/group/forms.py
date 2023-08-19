"""
Formularios para Perfiles(groups) de usuario

Formularios
-----------
frmGroup
    Formulario Completo
    - name
    - permissions
"""
from django import forms

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from zend_django.hiperforms import HorizontalModelForm


class frmGroup(HorizontalModelForm):
    """
    Formulario principal del grupo

    Campos
    ------
    - name
    - permissions
    """

    class Meta:
        model = Group
        fields = [
            'name',
            'permissions',
        ]
        labels: {
            'name': "Perfil",
            'permissions': "Permisos",
        }
        widgets = {
            'permissions': forms.SelectMultiple(attrs={"size": 25})
        }
