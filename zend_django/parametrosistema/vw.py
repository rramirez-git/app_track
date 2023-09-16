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
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from os import mkdir
from os import path

from .forms import frmParametroSistema as base_form
from .models import ParametroSistema as main_model
from .models import parametro_upload_to
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate


def template_base_path(file):
    return 'zend_django/parametrosistema/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Parámetros"
    titulo_descripcion = "de sistema"
    main_data_model = main_model
    model_name = "parametrosistema"
    app = 'administrar'

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(seccion__icontains=search_value) |
                Q(nombre__icontains=search_value) |
                Q(nombre_para_mostrar__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Parámetro"
    model_name = "parametrosistema"
    base_data_form = base_form
    main_data_model = main_model
    app = 'administrar'


class Create(GenericCreate):
    titulo = "Parámetro de sistema"
    model_name = "parametrosistema"
    base_data_form = base_form
    app = 'administrar'


class Update(GenericUpdate):
    titulo = "Parámetro de sistema"
    model_name = "parametrosistema"
    base_data_form = base_form
    main_data_model = main_model
    app = 'administrar'


class Delete(GenericDelete):
    model_name = "parametrosistema"
    main_data_model = main_model


class Set(View):
    """
    Vista para establecer los valores de los Parámetros de Sistema.

    Miembros
    --------
    - html_template = template_base_path("set")
    - titulo = "Parámetros"
    - titulo_descripcion = "de sistema (establecer)"
    - main_data_model = main_model
    - model_name = "parametrosistema"

    Métodos
    -------
    - get(request)
    - post(request)
    """
    html_template = template_base_path("set")
    titulo = "Parámetros"
    titulo_descripcion = "de sistema (establecer)"
    main_data_model = main_model
    model_name = "parametrosistema"
    app = 'configuracion'

    def get(self, request):
        data = list(self.main_data_model.objects.filter(es_multiple=False))
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': [],
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'singles': data,
            'app': self.app,
        })

    def post(self, request):
        if "singles" == request.POST.get('action'):
            parametros = self.main_data_model.objects.filter(es_multiple=False)
            for parametro in parametros:
                if ("INTEGER" == parametro.tipo.tipo_interno
                        or "STRING" == parametro.tipo.tipo_interno
                        or "DECIMAL" == parametro.tipo.tipo_interno
                        or "TEXT" == parametro.tipo.tipo_interno):
                    valor = request.POST.get(
                        f'{parametro.seccion}_{parametro.nombre}')
                    if valor is not None:
                        parametro.valor = valor
                        parametro.save()
                elif ("PICTURE" == parametro.tipo.tipo_interno
                        or "FILE" == parametro.tipo.tipo_interno):
                    file = request.FILES.get(
                        f'{parametro.seccion}_{parametro.nombre}')
                    if file is not None:
                        filename = path.join(
                            settings.MEDIA_ROOT,
                            parametro_upload_to,
                            file.name.replace(
                                " ", "_"))
                        bname = path.splitext(filename)[0]
                        if not path.exists(path.join(
                                settings.MEDIA_ROOT, parametro_upload_to)):
                            mkdir(path.join(
                                settings.MEDIA_ROOT, parametro_upload_to))
                        cont = 0
                        while path.isfile(filename):
                            cont += 1
                            fname, fext = path.splitext(filename)
                            filename = path.join(
                                settings.MEDIA_ROOT,
                                parametro_upload_to,
                                f"{bname}_{cont:04d}{fext}")
                        with open(filename, 'wb+') as archivo:
                            try:
                                for chunk in file.chunks:
                                    archivo.write(chunk)
                            except Exception:
                                archivo.write(file.read())
                        parametro.valor = path.join(
                            parametro_upload_to, path.basename(filename))
                        parametro.save()
        return self.get(request)
