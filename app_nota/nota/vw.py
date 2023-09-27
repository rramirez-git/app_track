from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate

from .forms import frmNota as base_form
from .models import Nota as main_model


def template_base_path(file):
    return 'app_nota/nota/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Notas"
    main_data_model = main_model
    model_name = "nota"
    app = 'nota'

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
    titulo_descripcion = "Nota"
    model_name = "nota"
    base_data_form = base_form
    main_data_model = main_model
    app = 'nota'
    html_template = template_base_path("read")


class Create(GenericCreate):
    titulo = "Nota"
    model_name = "nota"
    base_data_form = base_form
    app = 'nota'

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
    titulo = "Nota"
    model_name = "nota"
    base_data_form = base_form
    main_data_model = main_model
    app = 'nota'

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
    model_name = "nota"
    main_data_model = main_model
    app = 'nota'
