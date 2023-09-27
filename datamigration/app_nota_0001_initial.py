from django.contrib.auth.models import Permission

from app_catalogo.models import TipoParametro
from zend_django.models import MenuOpc
from zend_django.models import ParametroUsuario

from .utils import update_permisos


def migration():
    update_permisos()
    app = MenuOpc.objects.get_or_create(
        nombre="Notas", posicion=51, vista='idx_app_nota')[0]
    opc = MenuOpc.objects.get_or_create(
        nombre="Notas",
        vista="nota_list",
        posicion=1,
        padre=app
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_nota'),
        Permission.objects.get(codename='change_nota'),
        Permission.objects.get(codename='delete_nota'),
        Permission.objects.get(codename='view_nota'),
    ])

    tpCadena = TipoParametro.objects.get_or_create(
        nombre="Cadena", tipo_interno="STRING")[0]
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="nota", tipo=tpCadena)
