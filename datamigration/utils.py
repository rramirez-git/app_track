from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from zend_django.templatetags.op_labels import CRUD_labels


def migration():
    pass


def update_permisos():
    perfilSuperAdmin = Group.objects.get_or_create(
        name="SuperAdministrador")[0]
    perfilSuperAdmin.permissions.set(
        Permission.objects.all())
    perfilSuperAdmin = Group.objects.get_or_create(
        name="Solo Lectura")[0]
    perfilSuperAdmin.permissions.set(
        Permission.objects.filter(codename__icontains='view_'))

    for prefijo in [
            ('add_', 'Agregar', ),
            ('change_', CRUD_labels['update'], ),
            ('delete_', CRUD_labels['delete'], ),
            ('view_', CRUD_labels['read'], ), ]:
        for p in Permission.objects.filter(codename__icontains=prefijo[0]):
            p.name = str(p.name).replace('Can add', prefijo[1])
            p.save()
