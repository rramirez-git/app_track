"""
Definición de vistas genéricas, a partir de las cuales se generan las vistas
básicas de administración de los modelos definidos para las aplicaciones

Vistas
------
- GenericList
- GenericRead
- GenericCreate
- GenericUpdate
- GenericDelete
- Migrate
- GenericAppRootView
"""
import abc
import importlib
import os

from abc import ABCMeta
from datetime import datetime
from django.db import IntegrityError
from django.db import connection
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from os import path

from .parametrousuario.models import ParametroUsuario
from zend_django.templatetags.op_helpers import crud_label
from zend_django.templatetags.utils import GenerateReadCRUDToolbar


class GenericList(View):
    """
    Listado de obetos

    Miembros
    --------
    - html_template = ""
    - titulo = ""
    - titulo_descripcion = ""
    - main_data_model = None
    - model_name = ""
    - app = None

    Métodos
    -------
    - *get_data(search_value="") : []
    - base_render(request, data, search_value)
    - get(request)
    - *post(request)
    """
    html_template = ""
    titulo = ""
    titulo_descripcion = ""
    main_data_model = None
    model_name = ""
    app = None

    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def get_data(self, search_value=''):
        pass

    def base_render(self, request, data, search_value):
        ParametroUsuario.set_valor(
                request.user, 'basic_search', self.model_name, search_value)
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': [{'type': 'search'}],
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': search_value,
            'data': data,
            'app': self.app,
        })

    def get(self, request):
        search_value = ParametroUsuario.get_valor(
            request.user, 'basic_search', self.model_name)
        return self.base_render(
            request, self.get_data(search_value), search_value)

    def post(self, request):
        if "search" == request.POST.get('action', ''):
            search_value = request.POST.get('valor', '')
        else:
            search_value = ParametroUsuario.get_valor(
                request.user, 'basic_search', self.model_name)
        return self.base_render(
            request, self.get_data(search_value), search_value)


class GenericRead(View):
    """
    Visualización de objetos

    Miembros
    --------
    - html_template = "zend_django/html/form.html"
    - titulo_descripcion = ""
    - model_name = ""
    - base_data_form = None
    - main_data_model = None
    - app = None

    Métodos
    -------
    - get(request, pk)
    """
    html_template = "zend_django/html/form.html"
    titulo_descripcion = ""
    model_name = ""
    base_data_form = None
    main_data_model = None
    app = None

    __metaclass__ = ABCMeta

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj)
        toolbar = GenerateReadCRUDToolbar(
            request, self.model_name, obj, self.main_data_model)
        return render(request, self.html_template, {
            'titulo': obj,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': toolbar,
            'footer': False,
            'read_only': True,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': {'top': [{'form': form}]},
            'app': self.app,
            'object': obj,
            'withoutBtnSave': True,
        })


class GenericCreate(View):
    """
    Creación de objetos

    Miembros
    --------
    - html_template = "zend_django/html/form.html"
    - titulo = ""
    - model_name = ""
    - base_data_form = None
    - app = None

    Métodos
    -------
    - base_render(request, forms)
    - get(request)
    - post(request)
    """
    html_template = "zend_django/html/form.html"
    titulo = ""
    model_name = ""
    base_data_form = None
    app = None

    __metaclass__ = ABCMeta

    def base_render(self, request, forms):
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': crud_label('create'),
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': forms,
            'app': self.app,
        })

    def get(self, request):
        return self.base_render(request, {
            'top': [{'form': self.base_data_form()}]})

    def post(self, request):
        form = self.base_data_form(request.POST, files=request.FILES)
        if form.is_valid():
            try:
                obj = form.save()
                return HttpResponseRedirect(reverse(
                    f'{self.model_name}_read',
                    kwargs={'pk': obj.pk}))
            except IntegrityError as e:
                form.add(error=str(e))
        return self.base_render(request, {'top': [{'form': form}]})


class GenericUpdate(View):
    """
    Actualización de objetos

    Miembros
    --------
    - html_template = "zend_django/html/form.html"
    - titulo = ""
    - model_name = ""
    - base_data_form = None
    - main_data_model = None
    - app = None

    Métodos
    -------
    - base_render(request, form)
    - get(request, pk)
    - post(request, pk)
    """
    html_template = "zend_django/html/form.html"
    titulo = ""
    model_name = ""
    base_data_form = None
    main_data_model = None
    app = None

    __metaclass__ = ABCMeta

    def base_render(self, request, form, obj):
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': crud_label('update'),
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': {'top': [{'form': form}]},
            'app': self.app,
            'object': obj,
        })

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj)
        return self.base_render(request, form, obj)

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(
            instance=obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                obj = form.save()
                return HttpResponseRedirect(reverse(
                    f'{self.model_name}_read',
                    kwargs={'pk': obj.pk}))
            except IntegrityError as e:
                form.add_error(None, str(e))
        return self.base_render(request, form, obj)


class GenericDelete(View):
    """
    Borrado/Eliminado de objetos

    Miembros
    --------
    - model_name = ""
    - main_data_model = None

    Métodos
    -------
    - get(request, pk)
    """
    model_name = ""
    main_data_model = None

    __metaclass__ = ABCMeta

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        try:
            obj.delete()
            return HttpResponseRedirect(reverse(f'{self.model_name}_list'))
        except ProtectedError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))
        except IntegrityError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))


class Migrate(View):
    """
    Vista para la aplicación de migraciones de datos

    Miembros
    --------
    - migr_dir = 'datamigration'
    - app = None

    Métodos
    -------
    - agregar_a_db(filename)
    - verificar_en_db(filename)
    - aplicar(filename)
    - get(filename)
    """
    migr_dir = 'datamigration'
    app = 'configuracion'

    def agregar_a_db(self, filename):
        """
        Agregado de archivos de migracion a la base de datos

        Parameters
        ----------
        filename : string
            Archivo a agregar a la base de datos
        """
        filename = filename[:-3]
        sql = f"""
            INSERT INTO django_migrations(app, name, applied)
            VALUES (
                'data_migration',
                '{filename}',
                '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'
                );
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)

    def verificar_en_db(self, filename):
        """
        Verifica si un archivo ha sido cargado como migracion a través de
        su busqueda en base de datos.

        Parameters
        ----------
        filename : string
            Nombre del archivo a verficar

        Returns
        -------
        int
            Cantidad de veces que aparece el archivo en la base de datos
        """
        filename = filename[:-3]
        sql = f"""
            SELECT COUNT(*) AS n
            FROM django_migrations
            WHERE app = 'data_migration' AND name = '{filename}';
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return int(rows[0][0])

    def aplicar(self, filename):
        """
        Aplica (ejecuta) un archivo de migración

        Parameters
        ----------
        filename : string
            Archivo de migracion a aplicar

        Returns
        -------
        dict
            Diccionario con los resultados de la aplicacio en la forma
            {
                'file': filename
                'result': 'ok' o tipo de excepción en caso de error
            }
        """
        try:
            file = filename[0:-3]
            modulo = importlib.import_module(f'{self.migr_dir}.{file}')
            modulo.migration()
            result = "ok"
        except Exception as e:
            result = f'{type(e).__name__}: {e}'
        finally:
            return {
                'file': file,
                'result': result,
            }

    def get(self, request):
        migraciones = []
        for root, dirs, files in os.walk(
                path.join(os.getcwd(), self.migr_dir)):
            if path.join(os.getcwd(), self.migr_dir) == root:
                for f in files:
                    if "py" == f[-2:].lower():
                        if 0 == self.verificar_en_db(f):
                            result = self.aplicar(f)
                            migraciones.append(result)
                            if result['result'] == 'ok':
                                self.agregar_a_db(f)
                        else:
                            migraciones.append({
                                'file': f[:-3],
                                'result': 'previo',
                            })
        return render(request, 'zend_django/html/migracion.html', {
            'titulo': "Migraciones",
            'titulo_descripcion': '',
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'migraciones': migraciones,
            'app': self.app,
        })


class GenericAppRootView(View):
    """
    Vista incial de Apps

    Miembros
    --------
    - html_template = ""
    - titulo = ""
    - titulo_descripcion = ""
    - toolbar = None
    - app = None

    Métodos
    -------
    - base_render(request)
    - get(request)
    - post(request)
    """
    html_template = ""
    titulo = ""
    titulo_descripcion = ""
    toolbar = None
    app = None

    def base_render(self, request):
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': self.toolbar,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'app': self.app,
        })

    def get(self, request):
        return self.base_render(request)

    def post(self, request):
        return self.base_render(request)
