"""
Vistas relacionadas con el modelo User (Usuarios)

Vistas
------
- List
- Read
- Create
- Update
- Delete
- ResetPassword
"""
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import Group

from zend_django.user.forms import frmUser
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate
from zend_django.templatetags.utils import GenerateReadCRUDToolbar
from zend_django.templatetags.op_helpers import crud_label
from app_cliente.direccion.forms import frmDireccion

from .forms import frmCteGenerales as base_form
from .forms import frmCteUser
from .forms import frmCteOtros
from .forms import frmCteContacto
from .models import Cliente as main_model


def template_base_path(file):
    return 'app_cliente/cliente/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Clientes"
    titulo_descripcion = ""
    main_data_model = main_model
    model_name = "cliente"
    app = 'cliente'

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(userprofile__user__first_name__icontains=search_value) |
                Q(userprofile__user__last_name__icontains=search_value) |
                Q(userprofile__apellido_paterno__icontains=search_value) |
                Q(profile__apellido_materno__icontains=search_value) |
                Q(userprofile__user__email__icontains=search_value) |
                Q(userprofile__user__username__icontains=search_value) |
                Q(CURP__icontains=search_value) |
                Q(NSS__icontains=search_value) |
                Q(RFC__icontains=search_value)
                ).order_by('username'))


class Read(GenericRead):
    titulo_descripcion = "Cliente"
    model_name = "cliente"
    base_data_form = base_form
    main_data_model = main_model
    app = 'cliente'

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        fCUser = frmCteUser(
            instance=obj.userprofile.user,
            initial={
                'apellido_materno': obj.userprofile.apellido_materno,
                'password': obj.contraseña})
        fCGenerales = self.base_data_form(instance=obj)
        fCOtros = frmCteOtros(initial={
            'obs_semanas_cotizadas': obj.obs_semanas_cotizadas,
            'obs_homonimia': obj.obs_homonimia,
            'obs_duplicidad': obj.obs_duplicidad,
            'observaciones': obj.observaciones,
        })
        fCContacto = frmCteContacto(
            instance=obj.userprofile,
            initial={
                'email': obj.userprofile.user.email,
                'telefono_oficina': obj.telefono_oficina,
                'otro_telefono': obj.otro_telefono})
        fDireccion = frmDireccion(instance=obj.domicilio)
        forms = {
            'top': [{
                'title': 'Usuario',
                'form': fCUser}, ],
            'bottom': [{
                'title': 'Observaciones',
                'form': fCOtros}, ],
            'left': [{
                'title': 'Datos Generales',
                'form': fCGenerales}, ],
            'right': [
                {
                    'title': 'Contacto',
                    'form': fCContacto
                },
                {
                    'title': 'Dirección',
                    'form': fDireccion
                }, ],
        }
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
            'forms': forms,
            'app': self.app,
        })


class Create(GenericCreate):
    titulo = "Cliente"
    model_name = "cliente"
    base_data_form = base_form
    app = 'cliente'

    def get(self, request):
        fCUser = frmCteUser()
        fCGenerales = self.base_data_form()
        fCOtros = frmCteOtros()
        fCContacto = frmCteContacto()
        fDireccion = frmDireccion()
        forms = {
            'top': [{
                'title': 'Usuario',
                'form': fCUser}, ],
            'bottom': [{
                'title': 'Observaciones',
                'form': fCOtros}, ],
            'left': [{
                'title': 'Datos Generales',
                'form': fCGenerales}, ],
            'right': [
                {
                    'title': 'Contacto',
                    'form': fCContacto
                },
                {
                    'title': 'Dirección',
                    'form': fDireccion
                }, ],
        }
        return self.base_render(request, forms)

    def post(self, request):
        fCUser = frmCteUser(request.POST)
        fCGenerales = self.base_data_form(request.POST)
        fCOtros = frmCteOtros(request.POST)
        fCContacto = frmCteContacto(request.POST)
        fDireccion = frmDireccion(request.POST)
        forms = {
            'top': [{
                'title': 'Usuario',
                'form': fCUser}, ],
            'bottom': [{
                'title': 'Observaciones',
                'form': fCOtros}, ],
            'left': [{
                'title': 'Datos Generales',
                'form': fCGenerales}, ],
            'right': [
                {
                    'title': 'Contacto',
                    'form': fCContacto
                },
                {
                    'title': 'Dirección',
                    'form': fDireccion
                }, ],
        }
        if fCUser.is_valid() and fCGenerales.is_valid() and \
                fCOtros.is_valid() and fCContacto.is_valid() \
                and fDireccion.is_valid():
            user = fCUser.save()
            user.email = request.POST.get('email', '')
            user.set_password(request.POST.get('password', ''))
            user.groups.set((Group.objects.get(name="Cliente"), ))
            user.save()
            userprofile = fCContacto.save(commit=False)
            userprofile.user = user
            userprofile.apellido_materno = request.POST.get(
                'apellido_materno', '')
            userprofile.save()
            direccion = fDireccion.save()
            obj = fCGenerales.save(commit=False)
            obj.userprofile = userprofile
            obj.domicilio = direccion
            obj.contraseña = request.POST.get('password', '')
            obj.telefono_oficina = request.POST.get('telefono_oficina', '')
            obj.otro_telefono = request.POST.get('otro_telefono', '')
            obj.observaciones = request.POST.get(
                "observaciones", "")
            obj.obs_semanas_cotizadas = request.POST.get(
                "obs_semanas_cotizadas", "")
            obj.obs_homonimia = request.POST.get(
                "obs_homonimia", "")
            obj.obs_duplicidad = request.POST.get(
                "obs_duplicidad", "")
            obj.save()
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, forms)


class Update(GenericUpdate):
    titulo = "Cliente"
    model_name = "cliente"
    main_data_model = main_model
    base_data_form = base_form
    app = 'cliente'

    def base_render(self, request, forms):
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': crud_label('update'),
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': forms,
            'app': self.app
        })

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        fCUser = frmCteUser(
            instance=obj.userprofile.user,
            initial={
                'apellido_materno': obj.userprofile.apellido_materno,
                'password': obj.contraseña})
        fCGenerales = self.base_data_form(instance=obj)
        fCOtros = frmCteOtros(initial={
            'obs_semanas_cotizadas': obj.obs_semanas_cotizadas,
            'obs_homonimia': obj.obs_homonimia,
            'obs_duplicidad': obj.obs_duplicidad,
            'observaciones': obj.observaciones,
        })
        fCContacto = frmCteContacto(
            instance=obj.userprofile,
            initial={
                'email': obj.userprofile.user.email,
                'telefono_oficina': obj.telefono_oficina,
                'otro_telefono': obj.otro_telefono})
        fDireccion = frmDireccion(instance=obj.domicilio)
        forms = {
            'top': [{
                'title': 'Usuario',
                'form': fCUser}, ],
            'bottom': [{
                'title': 'Observaciones',
                'form': fCOtros}, ],
            'left': [{
                'title': 'Datos Generales',
                'form': fCGenerales}, ],
            'right': [
                {
                    'title': 'Contacto',
                    'form': fCContacto
                },
                {
                    'title': 'Dirección',
                    'form': fDireccion
                }, ],
        }
        return self.base_render(request, forms)

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj, data=request.POST)
        fCUser = frmCteUser(
            instance=obj.userprofile.user,
            initial={
                'apellido_materno': obj.userprofile.apellido_materno,
                'password': obj.contraseña},
            data=request.POST)
        fCGenerales = self.base_data_form(instance=obj,
        data=request.POST)
        fCOtros = frmCteOtros(initial={
            'obs_semanas_cotizadas': obj.obs_semanas_cotizadas,
            'obs_homonimia': obj.obs_homonimia,
            'obs_duplicidad': obj.obs_duplicidad,
            'observaciones': obj.observaciones,
            },
            data=request.POST)
        fCContacto = frmCteContacto(
            instance=obj.userprofile,
            initial={
                'email': obj.userprofile.user.email,
                'telefono_oficina': obj.telefono_oficina,
                'otro_telefono': obj.otro_telefono},
            data=request.POST)
        fDireccion = frmDireccion(
            instance=obj.domicilio,
            data=request.POST)
        forms = {
            'top': [{
                'title': 'Usuario',
                'form': fCUser}, ],
            'bottom': [{
                'title': 'Observaciones',
                'form': fCOtros}, ],
            'left': [{
                'title': 'Datos Generales',
                'form': fCGenerales}, ],
            'right': [
                {
                    'title': 'Contacto',
                    'form': fCContacto
                },
                {
                    'title': 'Dirección',
                    'form': fDireccion
                }, ],
        }
        if fCUser.is_valid() and fCGenerales.is_valid() and \
                fCOtros.is_valid() and fCContacto.is_valid() \
                and fDireccion.is_valid():
            user = fCUser.save()
            user.email = request.POST.get('email', '')
            user.set_password(request.POST.get('password', ''))
            user.groups.set((Group.objects.get(name="Cliente"), ))
            user.save()
            userprofile = fCContacto.save()
            userprofile.apellido_materno = request.POST.get(
                'apellido_materno', '')
            userprofile.save()
            direccion = fDireccion.save()
            obj = fCGenerales.save()
            obj.userprofile = userprofile
            obj.domicilio = direccion
            obj.contraseña = request.POST.get('password', '')
            obj.telefono_oficina = request.POST.get('telefono_oficina', '')
            obj.otro_telefono = request.POST.get('otro_telefono', '')
            obj.observaciones = request.POST.get(
                "observaciones", "")
            obj.obs_semanas_cotizadas = request.POST.get(
                "obs_semanas_cotizadas", "")
            obj.obs_homonimia = request.POST.get(
                "obs_homonimia", "")
            obj.obs_duplicidad = request.POST.get(
                "obs_duplicidad", "")
            obj.save()
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, forms)


class Delete(GenericDelete):
    model_name = "cliente"
    main_data_model = main_model

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        userprofile = obj.userprofile
        user = userprofile.user
        try:
            obj.delete()
            userprofile.delete()
            user.delete()
            return HttpResponseRedirect(reverse(f'{self.model_name}_list'))
        except ProtectedError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))
        except IntegrityError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))
