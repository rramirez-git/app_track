from datetime import date
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from routines.utils import as_paragraph_fn
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate

from .forms import frmAlerta as base_form
from .models import Alerta as main_model


def template_base_path(file):
    return 'app_alerta/alerta/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Alerta"
    main_data_model = main_model
    model_name = "alerta"
    app = 'alerta'

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(nota__icontains=search_value) |
                Q(user__first_name__icontains=search_value) |
                Q(user__last_name__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Alerta"
    model_name = "alerta"
    base_data_form = base_form
    main_data_model = main_model
    app = 'alerta'
    html_template = template_base_path("read")


class Create(GenericCreate):
    titulo = "Alerta"
    model_name = "alerta"
    base_data_form = base_form
    app = 'alerta'

    def post(self, request):
        form = self.base_data_form(request.POST, files=request.FILES)
        if form.is_valid():
            try:
                obj = form.save()
                obj.creado_por = request.user.get_full_name()
                obj.actualizado_por = request.user.get_full_name()
                obj.save()
                return HttpResponseRedirect(reverse(
                    f'{self.model_name}_read',
                    kwargs={'pk': obj.pk}))
            except IntegrityError as e:
                form.add(error=str(e))
        return self.base_render(request, {'top': [{'form': form}]})


class Update(GenericUpdate):
    titulo = "Alerta"
    model_name = "alerta"
    base_data_form = base_form
    main_data_model = main_model
    app = 'alerta'

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(
            instance=obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                obj = form.save()
                obj.actualizado_por = request.user.get_full_name()
                obj.save()
                return HttpResponseRedirect(reverse(
                    f'{self.model_name}_read',
                    kwargs={'pk': obj.pk}))
            except IntegrityError as e:
                form.add_error(None, str(e))
        return self.base_render(request, form, obj)


class Delete(GenericDelete):
    model_name = "alerta"
    main_data_model = main_model
    app = 'alerta'


class GetAvailableAlertas(View):
    def get(self, request):
        for alerta in request.user.alertas.filter(
                mostrar_alerta=True,
                fecha_alerta__lte=date.today(),
                alertado=False):
            alerta.alertado = True
            alerta.fecha_alertado = date.today()
            alerta.updated_by = request.user.get_full_name()
            alerta.save()
        return JsonResponse([
            {'pk': alerta.pk, 'nota': as_paragraph_fn(alerta.nota)}
            for alerta in request.user.alertas.filter(
                mostrar_alerta=True, fecha_alerta__lte=date.today())
            ], safe=False)


class DiabledAlerta(View):
    def get(self, request, pk):
        if not request.user.alertas.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        alerta = request.user.alertas.get(pk=pk)
        alerta.mostrar_alerta = False
        alerta.fecha_no_mostrar = date.today()
        alerta.updated_by = request.user.get_full_name()
        alerta.save()
        return HttpResponseRedirect(reverse('session_imin'))
