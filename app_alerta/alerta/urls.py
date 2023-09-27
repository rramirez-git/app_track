"""
URL's para el modulo de administración de Alertas
Se generan las url para CRUD con los permisos requeridos

obj = 'alerta'
app_label = 'app_alerta'

base_path => alerta/

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

import app_alerta.alerta.vw as views

obj = 'alerta'
app_label = 'app_alerta'

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
    path('obtener/', permission_required(
        f'{app_label}.get_{obj}')(views.GetAvailableAlertas.as_view()),
        name=f"{obj}_get"),
    path('desactivar/<pk>/', permission_required(
        f'{app_label}.disabled_{obj}')(views.DiabledAlerta.as_view()),
        name=f"{obj}_disabled"),
    path('<pk>/', permission_required(
        f'{app_label}.view_{obj}')(views.Read.as_view()),
        name=f"{obj}_read"),
]
