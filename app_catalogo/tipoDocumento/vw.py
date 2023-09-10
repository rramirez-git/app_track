from django.db.models import Q

from app_catalogo.views import GenericCatalog

from .forms import frmCatalogo as main_form
from .models import TipoDocumento as main_model


def filterFn(view_object, model_objects, search_value):
    return model_objects.filter(
        Q(tipo_de_documento__icontains=search_value))


catalogo = GenericCatalog(
    'tipoDocumento', "Tipo de Documento",
    main_form, main_model, 'tipodocumento',
    filterFn)
