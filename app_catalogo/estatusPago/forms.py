from zend_django.hiperforms import HorizontalModelForm

from .models import EstatusPago as main_model


class frmCatalogo(HorizontalModelForm):

    class Meta:
        model = main_model
        fields = "__all__"
