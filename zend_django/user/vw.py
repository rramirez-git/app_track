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
from django.contrib.auth.models import User as main_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import frmUser as base_form
from .forms import frmUserBottom
from .forms import frmUserLeft
from .forms import frmUserResetPassword
from .forms import frmUserRight
from .forms import frmUserTop
from .forms import frmUserTopMe
from .forms import frmUserTopReadUpdate
from .forms import frmUserUpdate
from .models import UserProfile
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate
from zend_django.templatetags.op_helpers import action_label
from zend_django.templatetags.op_helpers import crud_icon
from zend_django.templatetags.op_helpers import crud_label
from zend_django.templatetags.op_helpers import crud_smart_button
from zend_django.templatetags.utils import GenerateReadCRUDToolbar


def template_base_path(file):
    return 'zend_django/user/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Usuarios"
    titulo_descripcion = ""
    main_data_model = main_model
    model_name = "user"
    app = 'administrar'

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all().order_by('username'))
        else:
            return list(self.main_data_model.objects.filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(profile__apellido_materno__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(username__icontains=search_value)).order_by('username'))


class Read(GenericRead):
    titulo_descripcion = "Usuario"
    model_name = "user"
    base_data_form = base_form
    main_data_model = main_model
    app = 'administrar'

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        try:
            obj.profile
        except ObjectDoesNotExist:
            UserProfile.objects.create(user=obj)
        form = {
            'top': frmUserTopReadUpdate(instance=obj),
            'bottom': frmUserBottom(instance=obj),
            'left': frmUserLeft(instance=obj, initial={
                'apellido_materno': obj.profile.apellido_materno,
                'telefono': obj.profile.telefono,
                'celular': obj.profile.celular,
                'whatsapp': obj.profile.whatsapp,
            }),
            'right': frmUserRight(instance=obj),
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
            'forms': {
                'top': [{'form': form['top']}],
                'bottom': [{'form': form['bottom']}],
                'left': [{'form': form['left']}],
                'right': [{'form': form['right']}],
            },
            'app': self.app,
        })


class Create(GenericCreate):
    titulo = "Usuario"
    model_name = "user"
    base_data_form = base_form
    app = 'administrar'

    def get(self, request):
        return self.base_render(request, {
                'top': [{'form': frmUserTop()}],
                'bottom': [{'form': frmUserBottom()}],
                'left': [{'form': frmUserLeft()}],
                'right': [{'form': frmUserRight()}],
            })

    def post(self, request):
        form = self.base_data_form(request.POST)
        form_aux = {
                'top': [{'form': frmUserTop(request.POST)}],
                'bottom': [{'form': frmUserBottom(request.POST)}],
                'left': [{'form': frmUserLeft(request.POST)}],
                'right': [{'form': frmUserRight(request.POST)}],
            }
        if form.is_valid():
            obj = form.save()
            obj.set_password(form.cleaned_data['password'])
            obj.save()
            UserProfile.objects.create(
                apellido_materno=form.cleaned_data['apellido_materno'],
                telefono=form.cleaned_data['telefono'],
                celular=form.cleaned_data['celular'],
                whatsapp=form.cleaned_data['whatsapp'],
                user=obj
            )
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, form_aux)


class Update(GenericUpdate):
    titulo = "Usuario"
    model_name = "user"
    main_data_model = main_model
    app = 'administrar'

    def base_render(self, request, form):
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': crud_label('update'),
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': {
                'bottom': [{'form': form['bottom']}],
                'left': [{'form': form['left']}],
                'right': [{'form': form['right']}],
            },
            'app': self.app
        })

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = {
            'bottom': frmUserBottom(instance=obj),
            'left': frmUserLeft(instance=obj, initial={
                'apellido_materno': obj.profile.apellido_materno,
                'telefono': obj.profile.telefono,
                'celular': obj.profile.celular,
                'whatsapp': obj.profile.whatsapp,
            }),
            'right': frmUserRight(instance=obj),
        }
        return self.base_render(request, form)

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = frmUserUpdate(instance=obj, data=request.POST)
        form_aux = {
            'bottom': frmUserBottom(request.POST),
            'left': frmUserLeft(request.POST),
            'right': frmUserRight(request.POST)
        }
        if form.is_valid():
            obj = form.save()
            obj.profile.apellido_materno = form.cleaned_data[
                'apellido_materno']
            obj.profile.telefono = form.cleaned_data['telefono']
            obj.profile.celular = form.cleaned_data['celular']
            obj.profile.whatsapp = form.cleaned_data['whatsapp']
            obj.profile.save()
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, form_aux)


class Delete(GenericDelete):
    model_name = "user"
    main_data_model = main_model


class ResetPassword(View):
    """
    Reseteo de contraseñas

    Miembros
    --------
    - main_data_model = User

    Métodos
    -------
    - base_render(request, form)
    - get(request, username='')
    - post(request, username='')
    """
    main_data_model = main_model
    app = 'configuracion'

    def base_render(self, request, form):
        return render(request, "zend_django/html/form.html", {
            'titulo': "Usuario",
            'titulo_descripcion': action_label('reset_password'),
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': {'top': [{'form': form}]},
            'app': self.app,
        })

    def get(self, request, username=''):
        return self.base_render(request, frmUserResetPassword(
            initial={'username': username}))

    def post(self, request, username=''):
        form = frmUserResetPassword(request.POST)
        if form.is_valid():
            obj = self.main_data_model.objects.filter(
                username=form.cleaned_data['username'])
            if obj.exists():
                obj = obj[0]
                obj.set_password(form.cleaned_data['password'])
                obj.save()
                return render(
                    request,
                    template_base_path('reset_password_ok'), {
                        'titulo': "Usuario",
                        'titulo_descripcion': action_label('reset_password'),
                        'toolbar': None,
                        'footer': False,
                        'read_only': False,
                        'alertas': [],
                        'req_chart': False,
                        'app': self.app,
                    })
            else:
                form.add_error('username', "No existe el usuario")
        return self.base_render(request, form)


class Me(GenericUpdate):
    titulo = "Mi Perfil"
    model_name = "user"
    main_data_model = main_model

    def base_render(self, request, form):
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': None,
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': {
                'top': [{'title': "Mi acceso", 'form': form['top']}],
                'bottom': [{'title': "Mis datos", 'form': form['bottom']}],
            },
            'app': self.app
        })

    def get(self, request):
        obj = request.user
        form = {
            'bottom': frmUserLeft(instance=obj, initial={
                'apellido_materno': obj.profile.apellido_materno,
                'telefono': obj.profile.telefono,
                'celular': obj.profile.celular,
                'whatsapp': obj.profile.whatsapp,
            }),
            'top': frmUserTopMe(initial={
                'username': obj.username,
            }),
        }
        return self.base_render(request, form)

    def post(self, request):
        obj = request.user
        form = {
            'bottom': frmUserLeft(instance=obj, data=request.POST),
            'top': frmUserTopMe(data=request.POST),
        }
        if form['bottom'].is_valid() and form['top'].is_valid():
            obj = form['bottom'].save()
            obj.username = form['top'].cleaned_data['username']
            if form['top'].cleaned_data['password']:
                obj.set_password(form['top'].cleaned_data['password'])
            obj.save()
            obj.profile.apellido_materno = form['bottom'].cleaned_data[
                'apellido_materno']
            obj.profile.telefono = form['bottom'].cleaned_data['telefono']
            obj.profile.celular = form['bottom'].cleaned_data['celular']
            obj.profile.whatsapp = form['bottom'].cleaned_data['whatsapp']
            obj.profile.save()
        return self.base_render(request, form)
