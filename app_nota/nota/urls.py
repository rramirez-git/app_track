"""
URL's para el modulo de administración de Notas
Se generan las url para CRUD con los permisos requeridos

obj = 'nota'
app_label = 'app_nota'

base_path => nota/

Perm => View => Path
--------------------
- view   => list   =>
- add    => create => nuevo/
- change => update => actualizar/<pk>/
- delete => delete => eliminar/<pk>/
- view   => read   => <pk>/

permiso_requerido = {app_label}.{Perm}_{obj}
vista = {obj}_{View}

"""
from django.contrib.auth.decorators import permission_required
from django.urls import path

import app_nota.nota.vw as views

obj = 'nota'
app_label = 'app_nota'

urlpatterns = [
    path('', permission_required(
        f'{app_label}.view_{obj}')(views.List.as_view()),
        name=f"{obj}_list"),
    path('nuevo/', permission_required(
        f'{app_label}.add_{obj}')(views.Create.as_view()),
        name=f"{obj}_create"),
    path('actualizar/<pk>/', permission_required(
        f'{app_label}.change_{obj}')(views.Update.as_view()),
        name=f"{obj}_update"),
    path('eliminar/<pk>/', permission_required(
        f'{app_label}.delete_{obj}')(views.Delete.as_view()),
        name=f"{obj}_delete"),
    path('<pk>/', permission_required(
        f'{app_label}.view_{obj}')(views.Read.as_view()),
        name=f"{obj}_read"),
]
