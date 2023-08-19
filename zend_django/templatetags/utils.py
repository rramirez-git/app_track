"""
Funciones de utilería para la aplicación
"""

from django.contrib.contenttypes.models import ContentType
from django.db import models
from functools import reduce

from zend_django.templatetags.op_helpers import crud_icon
from zend_django.templatetags.op_helpers import crud_label
from zend_django.templatetags.op_helpers import crud_smart_button


def GenerateReadCRUDToolbar(
        request, base_name, object, model, label_and_icon=False):
    """
    Genera el arreglo con las opciones CRUD para para la barra de herramientas
    desplegada, normalmente, en las vistas READ de la administración de los
    modelos

    Parameters
    ----------
    request : Request
        Request pasado como parámetro a la funcion de la vista

    base_name : string
        Nombre base del modelo

    pk : int
        Llave primaria del objeto en la vista, sobre el cual se generarán las
        llamadas a las vistas CRUD

    model : Model
        Modelo para con el cual se generará la barra de herramientas

    Returns
    -------
    list
        Lista con las opciones para generar la barra de herramientas con el
        tag {% include "zend_django/html/toolbar.html" %} a través del
        parámetro toolbar
    """
    toolbar = []
    content_type = ContentType.objects.get_for_model(model)
    if request.user.has_perm(
            f"{content_type.app_label}.view_{content_type.model}"):
        toolbar.append({
            'type': 'link',
            'view': f'{base_name}_list',
            'label': crud_smart_button(
                'list') if label_and_icon else crud_icon('list'),
            'title': crud_label('list')})
    if request.user.has_perm(
            f"{content_type.app_label}.change_{content_type.model}"):
        toolbar.append({
            'type': 'link_pk',
            'view': f'{base_name}_update',
            'pk': object.pk,
            'label': crud_smart_button(
                'update') if label_and_icon else crud_icon('update'),
            'title': crud_label('update')})
    if request.user.has_perm(
            f"{content_type.app_label}.delete_{content_type.model}"):
        toolbar.append({
            'type': 'link_pk_del',
            'view': f'{base_name}_delete',
            'pk': object.pk,
            'label': crud_smart_button(
                'delete') if label_and_icon else crud_icon('delete'),
            'title': crud_label('delete')})
    next = GetNextPrevObject(object)
    prev = GetNextPrevObject(object, True)
    if prev:
        toolbar.append({
            'type': 'link_pk',
            'label': '<i class="fas fa-chevron-left"></i>',
            'title': 'Anterior',
            'view': f'{base_name}_read',
            'pk': prev.pk})
    if next:
        toolbar.append({
            'type': 'link_pk',
            'label': '<i class="fas fa-chevron-right"></i>',
            'title': 'Siguiente',
            'view': f'{base_name}_read',
            'pk': next.pk})
    return toolbar


def get_model_attr(instance, attr):
    """Example usage: get_model_attr(instance, 'category__slug')"""
    for field in attr.split('__'):
        if instance is None:
            break
        instance = getattr(instance, field)
    return instance


def GetNextPrevObject(instance, prev=False, qs=None, loop=False):
    if not qs:
        qs = instance.__class__.objects.all()
    if prev:
        qs = qs.reverse()
        lookup = 'lt'
    else:
        lookup = 'gt'
    q_list = []
    prev_fields = []
    if qs.query.extra_order_by:
        ordering = qs.query.extra_order_by
    elif qs.query.order_by:
        ordering = qs.query.order_by
    elif qs.query.get_meta().ordering:
        ordering = qs.query.get_meta().ordering
    else:
        ordering = []
    ordering = list(ordering)
    if 'pk' not in ordering and '-pk' not in ordering:
        ordering.append('pk')
        qs = qs.order_by(*ordering)
    for field in ordering:
        if field[0] == '-':
            this_lookup = (lookup == 'gt' and 'lt' or 'gt')
            field = field[1:]
        else:
            this_lookup = lookup
        q_kwargs = dict([(f, get_model_attr(instance, f))
                         for f in prev_fields if get_model_attr(
                            instance, f) is not None])
        key = "%s__%s" % (field, this_lookup)
        q_kwargs[key] = get_model_attr(instance, field)
        if q_kwargs[key] is None:
            del(q_kwargs[key])
        q_list.append(models.Q(**q_kwargs))
        prev_fields.append(field)
    try:
        obj = qs.filter(reduce(models.Q.__or__, q_list))[0]
        return obj if instance.pk != obj.pk else None
    except IndexError:
        length = qs.count()
        if loop and length > 1:
            obj = qs[0]
            return obj if instance.pk != obj.pk else None
    return None
