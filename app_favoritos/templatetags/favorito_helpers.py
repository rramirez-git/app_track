"""
Funciones de ayuda para la generación, automaticación y correcta ejecución
del menú principal y sus opciones

Cargar con {% load favorito_helpers %}
"""
from django import template

from app_favoritos.manage.models import Favorito

register = template.Library()


@register.inclusion_tag(
    'app_favoritos/favs/main_menu_fav_links.html', takes_context=True)
def display_main_menu_fav_links(context, extra_class=''):
    data = list(Favorito.objects.filter(
        usuario=context.get('user')))
    return {'favs': data, 'extra_class': extra_class}
