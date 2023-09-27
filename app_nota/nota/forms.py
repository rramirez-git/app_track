from zend_django.hiperforms import HorizontalModelForm

from .models import Nota


class frmNota(HorizontalModelForm):

    class Meta:
        model = Nota
        fields = [
            'user',
            'nota',
        ]
