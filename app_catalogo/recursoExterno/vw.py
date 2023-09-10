from django.db.models import Q

from app_catalogo.views import GenericCatalog

from .forms import frmCatalogo as main_form
from .models import RecursoExterno as main_model


def filterFn(view_object, model_objects, search_value):
    return model_objects.filter(
        Q(nombre__icontains=search_value) |
        Q(apellido_paterno__icontains=search_value) |
        Q(apellido_materno__icontains=search_value))


catalogo = GenericCatalog(
    'recursoExterno', "Recurso Externo",
    main_form, main_model, 'recursoexterno',
    filterFn)
