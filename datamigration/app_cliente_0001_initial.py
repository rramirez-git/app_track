from django.contrib.auth.models import Permission

from .utils import update_permisos
from zend_django.models import MenuOpc


def migration():
    update_permisos()
    app = MenuOpc.objects.get_or_create(
        nombre="Clientes", posicion=50, vista='idx_app_cliente')[0]
    opc = MenuOpc.objects.get_or_create(
        nombre="Clientes",
        vista="cliente_list",
        posicion=1,
        padre=app
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_cliente'),
        Permission.objects.get(codename='change_cliente'),
        Permission.objects.get(codename='delete_cliente'),
        Permission.objects.get(codename='view_cliente'),
    ])
