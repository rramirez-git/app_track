"""
URL's para acceso a vista de la aplicacion app_alerta

base_path => '/'

"""
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path

from .views import AlertasView

urlpatterns = [
     path(
          'alertas/',
          login_required(AlertasView.as_view()),
          name="idx_app_alerta"),
     path('alerta/',
          include('app_alerta.alerta.urls')),
]
