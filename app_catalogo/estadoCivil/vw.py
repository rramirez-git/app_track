from django.db.models import Q

from app_catalogo.views import GenericCatalog

from .forms import frmCatalogo as main_form
from .models import EstadoCivil as main_model


def filterFn(view_object, model_objects, search_value):
    return model_objects.filter(
        Q(estado_civil__icontains=search_value))


catalogo = GenericCatalog(
    'estadoCivil', "Estado Civil",
    main_form, main_model, 'estadocivil',
    filterFn)
