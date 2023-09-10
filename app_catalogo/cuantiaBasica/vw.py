from django.db.models import Q

from app_catalogo.views import GenericCatalog

from .forms import frmCatalogo as main_form
from .models import CuantiaBasica as main_model


def filterFn(view_object, model_objects, search_value):
    return [
        obj
        for obj in model_objects.all()
        if float(obj.salario_inicio) <= float(search_value) <= float(obj.salario_fin)]


catalogo = GenericCatalog(
    'cuantiaBasica', "Cuantía Básica e Incremento Anual",
    main_form, main_model, 'cuantiabasica',
    filterFn)
