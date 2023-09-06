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

from zend_django.user.forms import frmUser
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate

from app_cliente.direccion.forms import frmDireccion

from .forms import frmCliente as base_form
from .forms import frmClienteContacto
from .forms import frmClienteObservaciones
from .forms import frmClienteOtro
from .forms import frmClienteTrabajo
from .forms import frmClienteUsuario
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
        forms = {
            'top': [{
                'title': 'Usuario',
                'form': frmClienteUsuario(instance=obj)}, ],
            'bottom': [{
                'title': 'Observaciones',
                'form': frmClienteObservaciones(instance=obj)}, ],
            'left': [{
                'title': 'Datos Generales',
                'form': frmClienteTrabajo(instance=obj)}, ],
            'right': [
                {
                    'title': 'Contacto',
                    'form': frmClienteContacto(instance=obj)
                    },
                {
                    'title': 'Dirección',
                    'form': frmDireccion(instance=obj.domicilio)
                    },
                {
                    'title': 'Otros',
                    'form': frmClienteOtro(instance=obj)
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
        forms = {
            'top': [{
                'title': 'Usuario',
                'form': frmClienteUsuario()}, ],
            'bottom': [{
                'title': 'Observaciones',
                'form': frmClienteObservaciones()}, ],
            'left': [{
                'title': 'Datos Generales',
                'form': frmClienteTrabajo()}, ],
            'right': [
                {
                    'title': 'Contacto',
                    'form': frmClienteContacto()
                    },
                {
                    'title': 'Dirección',
                    'form': frmDireccion()
                    },
                {
                    'title': 'Otros',
                    'form': frmClienteOtro()
                    }, ],
        }
        return self.base_render(request, forms)

    def post(self, request):
        form = self.base_data_form(request.POST)
        forms = {
            'top': [{
                'title': 'Usuario',
                'form': frmClienteUsuario(request.POST)}, ],
            'bottom': [{
                'title': 'Observaciones',
                'form': frmClienteObservaciones(request.POST)}, ],
            'left': [{
                'title': 'Datos Generales',
                'form': frmClienteTrabajo(request.POST)}, ],
            'right': [
                {
                    'title': 'Contacto',
                    'form': frmClienteContacto(request.POST)
                    },
                {
                    'title': 'Dirección',
                    'form': frmDireccion(request.POST)
                    },
                {
                    'title': 'Otros',
                    'form': frmClienteOtro(request.POST)
                    }, ],
        }
        if form.is_valid():
            user = frmUser(request.POST).save()
            user.set_password(form.cleaned_data['contraseña'])
            userprofile = UserProfile.objects.create(
                apellido_materno=form.cleaned_data['apellido_materno'],
                telefono=form.cleaned_data['telefono'],
                celular=form.cleaned_data['celular'],
                whatsapp=form.cleaned_data['whatsapp'],
                user=user
            )
            direccion = forms['right'][1]['form'].save()
            obj = form.save(commit=False)
            obj.userprofile = userprofile
            obj.direccion = direccion
            obj.save()
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, forms)


class Update(GenericUpdate):
    titulo = "Cliente"
    model_name = "cliente"
    main_data_model = main_model
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
        forms = {
            'top': [{
                'title': 'Usuario',
                'form': frmClienteUsuario(instance=obj)}, ],
            'bottom': [{
                'title': 'Observaciones',
                'form': frmClienteObservaciones(instance=obj)}, ],
            'left': [{
                'title': 'Datos Generales',
                'form': frmClienteTrabajo(instance=obj)}, ],
            'right': [
                {
                    'title': 'Contacto',
                    'form': frmClienteContacto(instance=obj)
                    },
                {
                    'title': 'Dirección',
                    'form': frmDireccion(instance=obj.domicilio)
                    },
                {
                    'title': 'Otros',
                    'form': frmClienteOtro(instance=obj)
                    }, ],
        }
        return self.base_render(request, forms)

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj, data=request.POST)
        forms = {
            'top': [{
                'title': 'Usuario',
                'form': frmClienteUsuario(
                    instance=obj, data=request.POST)}, ],
            'bottom': [{
                'title': 'Observaciones',
                'form': frmClienteObservaciones(
                    instance=obj, data=request.POST)}, ],
            'left': [{
                'title': 'Datos Generales',
                'form': frmClienteTrabajo(
                    instance=obj, data=request.POST)}, ],
            'right': [
                {
                    'title': 'Contacto',
                    'form': frmClienteContacto(
                        instance=obj, data=request.POST)
                    },
                {
                    'title': 'Dirección',
                    'form': frmDireccion(
                        instance=obj.direccion, data=request.POST)
                    },
                {
                    'title': 'Otros',
                    'form': frmClienteOtro(
                        instance=obj, data=request.POST)
                    }, ],
        }
        if form.is_valid():
            user = frmUser(
                instance=obj.userprofile.user, data=request.POST).save()
            user.set_password(form.cleaned_data['contraseña'])
            obj.userprofile.apellido_materno = form.cleaned_data[
                'apellido_materno'],
            obj.userprofile.telefono = form.cleaned_data['telefono']
            obj.userprofile.celular = form.cleaned_data['celular']
            obj.userprofile.whatsapp = form.cleaned_data['whatsapp']
            obj.userprofile.save()
            forms['right'][1]['form'].save()
            form.save()
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, forms)


class Delete(GenericDelete):
    model_name = "user"
    main_data_model = main_model

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        userprofile = obj.userprofile
        user = userprofile.user
        try:
            obj.delete()
            return HttpResponseRedirect(reverse(f'{self.model_name}_list'))
        except ProtectedError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))
        except IntegrityError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))
        try:
            userprofile.delete()
            return HttpResponseRedirect(reverse(f'{self.model_name}_list'))
        except ProtectedError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))
        except IntegrityError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))
        try:
            user.delete()
            return HttpResponseRedirect(reverse(f'{self.model_name}_list'))
        except ProtectedError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))
        except IntegrityError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))
