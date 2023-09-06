"""
URL's para acceso a vista de la aplicacion app_cliente

base_path => 'catalogo/'

"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.urls import include
from django.urls import path

from .views import CatalogosView

urlpatterns = [
     path(
          '',
          login_required(CatalogosView.as_view()),
          name="idx_app_catalogo"),
     path('tipo-de-expediente/',
          include('app_catalogo.taxonomiaExpediente.urls')),
]
