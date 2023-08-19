"""
Vistas relacionadas con el modelo Favorito

Vistas
------
- List
- Read
- Create
- Update
- Delete
"""
from django.db.models import Q

from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate

from .forms import frmFavorito as base_form
from .models import Favorito as main_model


def template_base_path(file):
    return 'app_favoritos/admin/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Favoritos"
    titulo_descripcion = ""
    main_data_model = main_model
    model_name = "favorito"
    app = 'administrar'

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(usuario__first_name__icontains=search_value) |
                Q(usuario__last_name__icontains=search_value) |
                Q(usuario__profile__apellido_materno__icontains=search_value) |
                Q(etiqueta__icontains=search_value) |
                Q(url__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Favorito"
    model_name = "favorito"
    base_data_form = base_form
    main_data_model = main_model
    app = 'administrar'


class Create(GenericCreate):
    titulo = "Favorito"
    model_name = "favorito"
    base_data_form = base_form
    app = 'administrar'


class Update(GenericUpdate):
    titulo = "Favorito"
    model_name = "favorito"
    base_data_form = base_form
    main_data_model = main_model
    app = 'administrar'


class Delete(GenericDelete):
    model_name = "favorito"
    main_data_model = main_model
