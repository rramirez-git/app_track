"""
URL's para acceso a vista de la aplicacion app_cliente

base_path =>

"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.urls import include
from django.urls import path

from .views import ClientesView

urlpatterns = [
     path('cliente/', include('app_cliente.cliente.urls')),
     path(
          'clientes-principal/',
          login_required(ClientesView.as_view()),
          name="idx_app_cliente"),
]
