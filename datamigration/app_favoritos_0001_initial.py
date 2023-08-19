from django.contrib.auth.models import Permission

from .utils import update_permisos
from zend_django.models import MenuOpc


def migration():
    update_permisos()
    opc = MenuOpc.objects.get_or_create(
        nombre="Favoritos",
        vista="favorito_list",
        posicion=7,
        padre=MenuOpc.objects.get(
            nombre='Administrar', vista='idx_app_administracion')
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_favorito'),
        Permission.objects.get(codename='change_favorito'),
        Permission.objects.get(codename='delete_favorito'),
        Permission.objects.get(codename='view_favorito'),
    ])
    opc = MenuOpc.objects.get_or_create(
        nombre="Mis Favoritos",
        vista="fav_list",
        posicion=1002
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_mine_fav'),
        Permission.objects.get(codename='change_mine_fav'),
        Permission.objects.get(codename='delete_mine_fav'),
        Permission.objects.get(codename='view_mine_fav'),
    ])
