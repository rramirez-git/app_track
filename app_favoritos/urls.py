"""
URL's para acceso a vista de la aplicacion zend_django

base_path =>
"""

from django.urls import include
from django.urls import path

urlpatterns = [
    path('favs/admin/', include('app_favoritos.manage.urls')),
    path('favs/', include('app_favoritos.favs.urls')),
]
