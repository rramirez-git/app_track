"""
Vistas relacionadas con el modelo Favorito, propios del usuario en sesion

Vistas
------
- List
- Read
- Create
- Update
- Delete
- Set
- Get
"""
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate
from zend_django.views import View

from app_favoritos.manage.models import Favorito as main_model
from .forms import frmFavorito as base_form
from zend_django.parametrousuario.models import ParametroUsuario


def template_base_path(file):
    return 'app_favoritos/favs/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Mis Favoritos"
    titulo_descripcion = ""
    main_data_model = main_model
    model_name = "favorito"
    app = 'mis_favoritos'

    def get_data(self, search_value='', usuario=None):
        if '' == search_value:
            data = self.main_data_model.objects.all()
        else:
            data = self.main_data_model.objects.filter(
                Q(etiqueta__icontains=search_value) |
                Q(url__icontains=search_value))
        return list(data.filter(usuario=usuario))

    def get(self, request):
        search_value = ParametroUsuario.get_valor(
            request.user, 'basic_search', self.model_name)
        return self.base_render(
            request, self.get_data(search_value, request.user), search_value)

    def post(self, request):
        if "search" == request.POST.get('action', ''):
            search_value = request.POST.get('valor', '')
        else:
            search_value = ParametroUsuario.get_valor(
                request.user, 'basic_search', self.model_name)
        return self.base_render(
            request, self.get_data(search_value, request.user), search_value)


class Read(GenericRead):
    titulo_descripcion = "Mi Favorito"
    model_name = "fav"
    base_data_form = base_form
    main_data_model = main_model
    app = 'mis_favoritos'


class Create(GenericCreate):
    titulo = "Mi Favorito"
    model_name = "fav"
    base_data_form = base_form
    app = 'mis_favoritos'

    def post(self, request):
        form = self.base_data_form(request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.save()
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, {'top': [{'form': form}]})


class Update(GenericUpdate):
    titulo = "Mi Favorito"
    model_name = "fav"
    base_data_form = base_form
    main_data_model = main_model
    app = 'mis_favoritos'


class Delete(GenericDelete):
    model_name = "fav"
    main_data_model = main_model


class Get(View):

    def base_render(self, request):
        return render(request, template_base_path('get'), {})

    def get(self, request):
        return self.base_render(request)

    def post(self, request):
        return self.base_render(request)


class Set(View):

    def base_render(self, request, etiqueta, url):
        main_model.objects.create(
            usuario=request.user,
            etiqueta=etiqueta,
            url=url
        )
        return render(request, template_base_path('get'), {})

    def get(self, request):
        return self.base_render(
            request, request.GET.get('etiqueta'), request.GET.get('url'))

    def post(self, request):
        return self.base_render(
            request, request.POST.get('etiqueta'), request.POST.get('url'))


class Del(View):

    def base_render(self, request, pk):
        main_model.objects.get(pk=pk).delete()
        return render(request, template_base_path('get'), {})

    def get(self, request):
        return self.base_render(request, request.GET.get('pk'))

    def post(self, request):
        return self.base_render(request, request.POST.get('pk'))
