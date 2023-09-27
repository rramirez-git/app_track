from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from app_catalogo.models import TipoParametro
from zend_django.models import MenuOpc
from zend_django.models import ParametroUsuario

from .utils import update_permisos


def migration():
    update_permisos()
    app = MenuOpc.objects.get_or_create(
        nombre="Alertas", posicion=52, vista='idx_app_alerta')[0]
    opc = MenuOpc.objects.get_or_create(
        nombre="Alertas",
        vista="alerta_list",
        posicion=1,
        padre=app
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_alerta'),
        Permission.objects.get(codename='change_alerta'),
        Permission.objects.get(codename='delete_alerta'),
        Permission.objects.get(codename='view_alerta'),
    ])

    tpCadena = TipoParametro.objects.get_or_create(
        nombre="Cadena", tipo_interno="STRING")[0]
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="alerta", tipo=tpCadena)

    gpo = Group.objects.get_or_create(name="Basico")[0]
    gpo.permissions.add(Permission.objects.get(codename='get_alerta'))
    gpo.permissions.add(Permission.objects.get(codename='disabled_alerta'))
