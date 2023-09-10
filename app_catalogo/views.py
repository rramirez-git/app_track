"""
Vistas relacionadas con el modelo ParametroSistema (Parámetros de Sistema)

Vistas
------
- List
- Read
- Create
- Update
- Delete
"""
from os import path

from zend_django.views import GenericAppRootView
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate


class CatalogosView(GenericAppRootView):
    html_template = "zend_django/idx_empty.html"
    titulo = "Catalogos"
    titulo_descripcion = ""
    toolbar = None
    app = 'catalogo'


def template_base_path(catalogo, file, path="app_catalogo"):
    return f'{path}/{catalogo}/{file}.html'


class GenericCatalog():
    def __init__(
            self, catalogo, titulo, base_form, main_model, model_name,
            filterFn,
            app='catalogo', descripcion=""):
        """
        filterFn    callable function for filtering objects
                    filterFn(model_objects, search_value)

                    def filterFn(view_object, model_objects, search_value):
                        return list(model_objects.filter(
                            Q(seccion__icontains=search_value) |
                            Q(nombre__icontains=search_value) |
                            Q(nombre_para_mostrar__icontains=search_value)))
        """
        self.catalogo = catalogo
        self.titulo = titulo
        self.descripcion = descripcion
        self.app = app
        self.base_form = base_form
        self.main_model = main_model
        self.model_name = model_name
        self.filterFn = filterFn

    def Read(self):
        class Read(GenericRead):
            titulo_descripcion = self.titulo
            model_name = self.model_name
            base_data_form = self.base_form
            main_data_model = self.main_model
            app = self.app
        return Read

    def Create(self):
        class Create(GenericCreate):
            titulo = self.titulo
            model_name = self.model_name
            base_data_form = self.base_form
            app = self.app
        return Create

    def Update(self):
        class Update(GenericUpdate):
            titulo = self.titulo
            model_name = self.model_name
            base_data_form = self.base_form
            main_data_model = self.main_model
            app = self.app
        return Update

    def Delete(self):
        class Delete(GenericDelete):
            model_name = self.model_name
            main_data_model = self.main_model
        return Delete

    def List(self):
        """
        filterFn    callable function for filtering objects
                    filterFn(model_objects, search_value)

                    def filterFn(view_object, model_objects, search_value):
                        return model_objects.filter(
                            Q(seccion__icontains=search_value) |
                            Q(nombre__icontains=search_value) |
                            Q(nombre_para_mostrar__icontains=search_value))
        """
        class List(GenericList):
            html_template = template_base_path(self.catalogo, "list")
            titulo = self.titulo
            main_data_model = self.main_model
            model_name = self.model_name
            app = self.app
            filterFn = self.filterFn

            def get_data(selfObj, search_value=''):
                if '' == search_value:
                    return list(
                        selfObj.main_data_model.objects.all())
                else:
                    return list(selfObj.filterFn(
                        selfObj.main_data_model.objects, search_value))
        return List
