"""
URL's para el modulo de administración de Colores Bootstrap
Se generan las url para CRUD con los permisos requeridos

obj = 'recursoexterno'
app_label = 'app_catalogo'

base_path => catalogo/recurso-externo/

Perm                               => View                 => Path
------------------------------------------------------------------
- view                             => list                 =>
- add                              => create               => nuevo/
- change                           => update               => actualizar/<pk>/
- delete                           => delete               => eliminar/<pk>/
- view                             => read                 => <pk>/

permiso_requerido = {app_label}.{Perm}_{obj}
vista = {obj}_{View}

"""
from django.contrib.auth.decorators import permission_required
from django.urls import path

from .vw import catalogo

obj = 'recursoexterno'
app_label = 'app_catalogo'

urlpatterns = [
    path('', permission_required(
        f'{app_label}.view_{obj}')(catalogo.List().as_view()),
        name=f"{obj}_list"),
    path('nuevo/', permission_required(
        f'{app_label}.add_{obj}')(catalogo.Create().as_view()),
        name=f"{obj}_create"),
    path('actualizar/<pk>/', permission_required(
        f'{app_label}.change_{obj}')(catalogo.Update().as_view()),
        name=f"{obj}_update"),
    path('eliminar/<pk>/', permission_required(
        f'{app_label}.delete_{obj}')(catalogo.Delete().as_view()),
        name=f"{obj}_delete"),
    path('<pk>/', permission_required(
        f'{app_label}.view_{obj}')(catalogo.Read().as_view()),
        name=f"{obj}_read"),
]
