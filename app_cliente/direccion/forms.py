from zend_django.hiperforms import HorizontalModelForm

from .models import Direccion


class frmDireccion(HorizontalModelForm):

    class Meta:
        model = Direccion
        fields = [
            'calle',
            'numero_exterior',
            'numero_interior',
            'codigo_postal',
            'colonia',
            'municipio',
            'estado',
        ]
