from django.db.models import Q

from app_catalogo.views import GenericCatalog

from .forms import frmCatalogo as main_form
from .models import TipoActividad as main_model


def filterFn(view_object, model_objects, search_value):
    return model_objects.filter(
        Q(tipo_de_actividad__icontains=search_value))


catalogo = GenericCatalog(
    'tipoActividad', "Tipo de Actividad",
    main_form, main_model, 'tipoactividad',
    filterFn)
