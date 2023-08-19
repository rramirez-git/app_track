"""
Vistas relacionadas con el modelo Group (Perifles de usuario)

Vistas
------
- List
- Read
- Create
- Update
- Delete
"""
from django.contrib.auth.models import Group as main_model
from django.contrib.auth.models import Permission
from django.db.models import Q

from .forms import frmGroup as base_form
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate


def template_base_path(file):
    return 'zend_django/group/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Perfiles"
    titulo_descripcion = "de usuario"
    main_data_model = main_model
    model_name = "group"
    app = 'administrar'

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(name__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Perfil"
    model_name = "group"
    base_data_form = base_form
    main_data_model = main_model
    app = 'administrar'


class Create(GenericCreate):
    titulo = "Perfil"
    model_name = 'group'
    base_data_form = base_form
    app = 'administrar'


class Update(GenericUpdate):
    titulo = "Perfil"
    model_name = "group"
    base_data_form = base_form
    main_data_model = main_model
    app = 'administrar'


class Delete(GenericDelete):
    model_name = "group"
    main_data_model = main_model
