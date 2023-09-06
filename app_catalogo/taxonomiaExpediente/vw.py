from app_catalogo.views import GenericCatalog

from .forms import frmTaxonomia
from .models import TaxonomiaExpediente


def filterFn(model_objects, search_value):
    return list(model_objects.filter(
        Q(nombre__icontains=search_value) |
        Q(descripcion__icontains=search_value)))


catalogo = GenericCatalog(
    'taxonomiaExpediente', "Tipos de Expediente",
    frmTaxonomia, TaxonomiaExpediente, 'taxonomiaexpediente',
    filterFn)
