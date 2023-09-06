from zend_django.hiperforms import HorizontalModelForm

from .models import TaxonomiaExpediente


class frmTaxonomia(HorizontalModelForm):

    class Meta:
        model = TaxonomiaExpediente
        fields = [
            'nombre',
            'color',
            'mostrar_en_panel',
            'descripcion',
        ]
