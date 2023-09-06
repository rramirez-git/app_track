from django.contrib.auth.models import Permission

from .utils import update_permisos
from zend_django.models import MenuOpc


def migration():
    update_permisos()
    cat = MenuOpc.objects.get_or_create(
        nombre="Catalogos", posicion=75, vista='idx_app_catalogo')[0]

    opc = MenuOpc.objects.get_or_create(
        nombre="Taxonomia Expediente",
        vista="taxonomiaexpediente_list",
        posicion=1,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_taxonomiaexpediente'),
        Permission.objects.get(codename='change_taxonomiaexpediente'),
        Permission.objects.get(codename='delete_taxonomiaexpediente'),
        Permission.objects.get(codename='view_taxonomiaexpediente'),
    ])
