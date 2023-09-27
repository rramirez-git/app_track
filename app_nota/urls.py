"""
URL's para acceso a vista de la aplicacion app_nota

base_path => '/'

"""
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path

from .views import NotasView

urlpatterns = [
     path(
          'notas/',
          login_required(NotasView.as_view()),
          name="idx_app_nota"),
     path('nota/',
          include('app_nota.nota.urls')),
]
