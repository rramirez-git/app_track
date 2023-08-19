"""
URL's para establecer y obtener opciones de favoritos y administrar los
favoritos propios del usuario

Se generan las url con los permisos requeridos para administrar los favoritos
propios del usuario en sesión y permisos de estar logeado para obtener y
establecer favoritos via json api post

obj = 'fav'
app_label = 'app_favoritos'

base_path => favs/

Perm          => View => Path
--------------------
- logged in   => set    => set/
- logged in   => get    => get/
- view_mine   => list   =>
- add_mine    => create => nuevo/
- change_mine => update => actualizar/<pk>/
- delete_mine => delete => eliminar/<pk>/
- view_mine   => read   => <pk>/

permiso_requerido = {app_label}.{Perm}_{obj}
vista = {obj}_{View}
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.urls import path

import app_favoritos.favs.vw as views

obj = 'fav'
app_label = 'app_favoritos'

urlpatterns = [
    path('', permission_required(
        f'{app_label}.view_mine_{obj}')(views.List.as_view()),
        name=f"{obj}_list"),
    path('nuevo/', permission_required(
        f'{app_label}.add_mine_{obj}')(views.Create.as_view()),
        name=f"{obj}_create"),
    path('actualizar/<pk>/', permission_required(
        f'{app_label}.change_mine_{obj}')(views.Update.as_view()),
        name=f"{obj}_update"),
    path('eliminar/<pk>/', permission_required(
        f'{app_label}.delete_mine_{obj}')(views.Delete.as_view()),
        name=f"{obj}_delete"),
    path('get/', login_required(
        views.Get.as_view()), name=f"{obj}_get"),
    path('set/', login_required(
        views.Set.as_view()), name=f"{obj}_set"),
    path('del/', login_required(
        views.Del.as_view()), name=f"{obj}_del"),
    path('<pk>/', permission_required(
        f'{app_label}.view_mine_{obj}')(views.Read.as_view()),
        name=f"{obj}_read"),
]
