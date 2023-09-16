from django.contrib.auth.models import Permission, Group

from zend_django.templatetags.op_labels import CRUD_labels


def migration():
    pass


def update_permisos():
    perfilSuperAdmin = Group.objects.get_or_create(name="SuperAdministrador")[0]
    perfilSuperAdmin.permissions.set(
        Permission.objects.all())
    perfilSuperAdmin = Group.objects.get_or_create(name="Solo Lectura")[0]
    perfilSuperAdmin.permissions.set(
        Permission.objects.filter(codename__icontains='view_'))

    for p in Permission.objects.filter(codename__icontains='add_'):
        p.name = str(p.name).replace('Can add', 'Agregar')
        p.save()

    for p in Permission.objects.filter(codename__icontains='change_'):
        p.name = str(p.name).replace('Can change', CRUD_labels['update'])
        p.save()

    for p in Permission.objects.filter(codename__icontains='delete_'):
        p.name = str(p.name).replace('Can delete', CRUD_labels['delete'])
        p.save()

    for p in Permission.objects.filter(codename__icontains='view_'):
        p.name = str(p.name).replace('Can view', CRUD_labels['read'])
        p.save()
