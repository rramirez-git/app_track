"""
Funciones de ayuda para la generación, automaticación y correcta ejecución
del menú principal y sus opciones

Cargar con {% load mainopc_helpers %}
"""
import json

from django import template
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User

from zend_django.menu.models import MenuOpc

register = template.Library()


@register.inclusion_tag(
    'zend_django/menuopc/list_opc.html', takes_context=True)
def print_menu_opc_adm(context, perms, opcion, nivel=-1):
    """
    Inclusion tag: {% print_menu_opc_adm perms opcion nivel %}
    Genera las etiquetas para generar el árbol de permisos con sangrias

    Parameters
    ----------
    context : ContextRequest
    perms : ContextRequest.perms
    opcion : MenuOpc
    nivel : int [-1]

    Returns
    -------
    dict
        Diccionario con las claves
            'nivel': int
            'reg': MenuOpc
            'perms': context[perms]
    """
    nivel += 1
    return {
        'nivel': nivel, 'reg': opcion, 'perms': perms
    }


def getMnuOpc4App(app):
    with open('managed/apps.json', 'r') as json_file:
        config = json.load(json_file)
    opc = MenuOpc.objects.filter(
        padre=None, posicion=config[app]['mnuopc_position'])
    return opc[0] if opc.exists() else None


@register.simple_tag
def get_app_name(app=None):
    if "" == app or app is None:
        return ""
    opc = getMnuOpc4App(app)
    return opc.nombre if opc is not None else ''


@register.inclusion_tag(
    'zend_django/menuopc/main_menu_opc.html', takes_context=True)
def main_menu(context, opciones=None, nivel=0, user_id=0, app=None):
    """
    Inclusion tag: {% main_menu opciones nivel user_id %}
    Genera las etiquetas para generar el menú principal en la barra superior

    Parameters
    ----------
    context : ContextRequest
    opciones : array_like MenuOpc
    nivel : int [0]
    user_id : int [0] User.pk
    app: string

    Returns
    -------
    dict
        Diccionario con las claves
            'nivel': int
            'opciones': array_like MenuOpc
            'user_id': int
            'app'
    """
    user = context.get('user')
    if user is None:
        user = user_id if isinstance(
            user_id, User) else User.objects.get(pk=user_id)
    if nivel == 0 and isinstance(user, AnonymousUser):
        return {}
    if opciones is None:
        if "" == app or app is None:
            opciones = []
        else:
            with open('managed/apps.json', 'r') as json_file:
                config = json.load(json_file)
            mnuOpc = MenuOpc.objects.filter(
                padre=None, posicion=config[app]['mnuopc_position'])
            if mnuOpc.exists():
                opciones = list(MenuOpc.objects.filter(padre=mnuOpc[0]))
            else:
                opciones = []
        nivel = 1
    else:
        nivel += 1
    opcs = []
    for opc in opciones:
        if opc.user_has_option(user):
            opcs.append(opc)
    return {
        'nivel': nivel,
        'opciones': opcs,
        'user_id': user.pk,
        'app': app
    }


@register.inclusion_tag(
    'zend_django/menuopc/get_apps.html', takes_context=True)
def get_apps(context, user_id=0):
    """
    Inclusion tag: {% get_apps %}
    Genera las etiquetas para generar el menú de Apps con base en las
    opciones de permisos en el menú principal
    Las opciones del menú en nivel 1 son las Apps

    Parameters
    ----------
    context : ContextRequest
    user_id : int [0] User.pk

    Returns
    -------
    dict
        Diccionario con las claves
            'apps': array_like MenuOpc de nivel 1 correspondientes
                        a las Apps
    """
    user = context.get('user')
    if user is None:
        user = user_id if isinstance(
            user_id, User) else User.objects.get(pk=user_id)
    if isinstance(user, AnonymousUser):
        return {}
    with open('managed/apps.json', 'r') as json_file:
        config = json.load(json_file)
    opciones = []
    for key, configApp in config.items():
        print(configApp)
        if configApp['display_as_app'] != hid:
            opciones.append(MenuOpc.objects.get(
                padre=None, posicion=configApp['mnuopc_position']))
    return {
        'apps': [opc for opc in opciones if opc.user_has_option(user)],
    }


@register.inclusion_tag(
    'zend_django/menuopc/get_apps.html', takes_context=True)
def get_apps(context, user_id=0):
    """
    Inclusion tag: {% get_apps %}
    Genera las etiquetas para generar el menú de Apps con base en las
    opciones de permisos en el menú principal
    Las opciones del menú en nivel 1 son las Apps

    Parameters
    ----------
    context : ContextRequest
    user_id : int [0] User.pk

    Returns
    -------
    dict
        Diccionario con las claves
            'apps': array_like MenuOpc de nivel 1 correspondientes
                        a las Apps
    """
    user = context.get('user')
    if user is None:
        user = user_id if isinstance(
            user_id, User) else User.objects.get(pk=user_id)
    if isinstance(user, AnonymousUser):
        return {}
    with open('managed/apps.json', 'r') as json_file:
        config = json.load(json_file)
    opciones = []
    for key, configApp in config.items():
        if configApp['display_as_app']:
            opc = MenuOpc.objects.filter(
                padre=None, posicion=configApp['mnuopc_position'])
            if opc.exists():
                opciones.append(opc[0])
    return {
        'apps': [opc for opc in opciones if opc.user_has_option(user)],
    }


@register.inclusion_tag(
    'zend_django/menuopc/get_apps_hidden.html', takes_context=True)
def get_hidden_apps(context, user_id=0):
    user = context.get('user')
    if user is None:
        user = user_id if isinstance(
            user_id, User) else User.objects.get(pk=user_id)
    if isinstance(user, AnonymousUser):
        return {}
    with open('managed/apps.json', 'r') as json_file:
        config = json.load(json_file)
    opciones = []
    for key, configApp in config.items():
        if not configApp['display_as_app']:
            opc = MenuOpc.objects.filter(
                padre=None, posicion=configApp['mnuopc_position'])
            if opc.exists():
                opciones.append(opc[0])
    return {
        'apps': [opc for opc in opciones if opc.user_has_option(user)],
    }
