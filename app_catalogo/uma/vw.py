from django.db.models import Q

from app_catalogo.views import GenericCatalog

from .forms import frmCatalogo as main_form
from .models import UMA as main_model


def filterFn(view_object, model_objects, search_value):
    return model_objects.filter(
        Q(año__icontains=search_value) |
        Q(valor__icontains=search_value))


catalogo = GenericCatalog(
    'uma', "Unidad de Medida y Actualización (UMA)",
    main_form, main_model, 'uma',
    filterFn)
