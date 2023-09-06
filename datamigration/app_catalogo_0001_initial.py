from zend_django.models import MenuOpc

from .utils import update_permisos


def migration():
    update_permisos()
    cat = MenuOpc.objects.get_or_create(
        nombre="Catalogos", posicion=75, vista='idx_app_catalogo')[0]
