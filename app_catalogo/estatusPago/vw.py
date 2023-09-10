from django.db.models import Q

from app_catalogo.views import GenericCatalog

from .forms import frmCatalogo as main_form
from .models import EstatusPago as main_model


def filterFn(view_object, model_objects, search_value):
    return model_objects.filter(
        Q(estatus_de_pago__icontains=search_value))


catalogo = GenericCatalog(
    'estatusPago', "Estatus de Pago",
    main_form, main_model, 'estatuspago',
    filterFn)
