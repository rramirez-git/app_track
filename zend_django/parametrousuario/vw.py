"""
Vistas relacionadas con el modelo ParametroUsuario (Parámetros de Usuario)

Vistas
------
- List
- Read
- Create
- Update
- Delete
"""
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from .models import ParametroUsuario as main_model
from .models import ParametroUsuarioValor
from .forms import frmParametroUsuario as base_form
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate


def template_base_path(file):
    return 'zend_django/parametrousuario/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Parámetros"
    titulo_descripcion = "de usuario"
    main_data_model = main_model
    model_name = "parametrousuario"
    app = 'administrar'

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(seccion__icontains=search_value) |
                Q(nombre__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Parámetro"
    model_name = "parametrousuario"
    base_data_form = base_form
    main_data_model = main_model
    app = 'administrar'


class Create(GenericCreate):
    titulo = "Parámetro de usuario"
    model_name = "parametrousuario"
    base_data_form = base_form
    app = 'administrar'


class Update(GenericUpdate):
    titulo = "Parámetro de usuario"
    model_name = "parametrousuario"
    base_data_form = base_form
    main_data_model = main_model
    app = 'administrar'


class Delete(GenericDelete):
    model_name = "parametrousuario"
    main_data_model = main_model


class SetValue(View):
    main_data_model = main_model

    def get(self, request):
        return JsonResponse({
            'status': 'error',
            'msg': "Metodo no implementado",
        }, safe=False)

    def post(self, request):
        seccion = request.POST.get('seccion')
        param = request.POST.get('parametro')
        usr = request.POST.get('user')
        valor = request.POST.get('value')
        if not (seccion and param and usr and valor):
            return JsonResponse({
                'status': 'error',
                'msg': "Alguno de los parametros requeridos no fue enviado",
                'extra': request.POST,
            }, safe=False)
        if not self.main_data_model.objects.filter(
                seccion=seccion, nombre=param).exists():
            return JsonResponse({
                'status': 'error',
                'msg': "El parametros requerido no fue encontrado",
                'extra': request.POST,
            }, safe=False)
        if not User.objects.filter(username=usr).exists():
            return JsonResponse({
                'status': 'error',
                'msg': "El usuario no fue encontrado",
                'extra': request.POST,
            }, safe=False)
        user = User.objects.get(username=usr)
        parametro = self.main_data_model.objects.get(
            seccion=seccion, nombre=param)
        pv = ParametroUsuarioValor.objects.get_or_create(
            parametro=parametro, user=user)[0]
        pv.valor = valor
        pv.save()
        return JsonResponse({
            'status': 'ok',
            'msg': "Valor actualizado",
            'extra': request.POST,
        }, safe=False)
