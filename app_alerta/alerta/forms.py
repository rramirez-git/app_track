from django import forms

from zend_django.hiperforms import HorizontalModelForm

from .models import Alerta


class frmAlerta(HorizontalModelForm):

    class Meta:
        model = Alerta
        fields = [
            'user',
            'nota',
            'fecha_alerta',
        ]
        widgets = {
            'fecha_alerta': forms.TextInput(attrs={'type': 'date'}),
        }
