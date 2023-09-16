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
     path('estado-civil/',
          include('app_catalogo.estadoCivil.urls')),
     path('cuantia-basica/',
          include('app_catalogo.cuantiaBasica.urls')),
     path('estatus-actividad/',
          include('app_catalogo.estatusActividad.urls')),
     path('factor-de-edad/',
          include('app_catalogo.factorEdad.urls')),
     path('medio-actividad/',
          include('app_catalogo.medioActividad.urls')),
     path('recurso-externo/',
          include('app_catalogo.recursoExterno.urls')),
     path('tipo-de-actividad/',
          include('app_catalogo.tipoActividad.urls')),
     path('tipo-de-documento/',
          include('app_catalogo.tipoDocumento.urls')),
     path('uma/',
          include('app_catalogo.uma.urls')),
     path('estatus-pago/',
          include('app_catalogo.estatusPago.urls')),
     path('cuenta-de-pago/',
          include('app_catalogo.cuentaPago.urls')),


     path('color-bootstrap/',
          include('app_catalogo.bootstrapColor.urls')),
     path('tipo-parametro/',
          include('app_catalogo.tipoParametro.urls')),
]
