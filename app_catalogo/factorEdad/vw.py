from django.db.models import Q

from app_catalogo.views import GenericCatalog

from .forms import frmCatalogo as main_form
from .models import FactorEdad as main_model


def filterFn(view_object, model_objects, search_value):
    return model_objects.filter(
        Q(edad=search_value))


catalogo = GenericCatalog(
    'factorEdad', "Porcentaje de Factor de Edad",
    main_form, main_model, 'factoredad',
    filterFn)
