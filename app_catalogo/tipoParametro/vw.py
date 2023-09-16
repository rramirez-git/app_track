from django.db.models import Q

from app_catalogo.views import GenericCatalog

from .forms import frmCatalogo as main_form
from .models import TipoParametro as main_model


def filterFn(view_object, model_objects, search_value):
    return model_objects.filter(
        Q(nombre__icontains=search_value) |
        Q(tipo_interno__icontains=search_value))


catalogo = GenericCatalog(
    'tipoParametro', "Tipos de Paramétro",
    main_form, main_model, 'tipoparametro',
    filterFn)
