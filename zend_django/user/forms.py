"""
Formularios para modelo User

Formularios
-----------
frmUser
    Formulario Completo
    - username
    - password
    - first_name
    - last_name
    - apellido_materno
    - email
    - telefono
    - celular
    - whatsapp
    - is_staff
    - is_active
    - is_superuser
    - groups
    - user_permissions

frmUserUpdate
    Formulario para actualizacion de usuarios
    - first_name
    - last_name
    - apellido_materno
    - email
    - telefono
    - celular
    - whatsapp
    - is_staff
    - is_active
    - is_superuser
    - groups
    - user_permissions

frmUserTop
    Formulario para desplegado en la sección Top
    - username
    - password

frmUserTopReadUpdate
    Formulario para desplegado en la sección Top (Read/Update)
    - username

frmUserLeft
    Formulario para desplegado en la sección Left
    - first_name
    - last_name
    - apellido_materno
    - email
    - telefono
    - celular
    - whatsapp

frmUserRight
    Formulario para desplegado en la sección Right
    - is_staff
    - is_active
    - is_superuser
    - groups

frmUserBottom
    Formulario para desplegado en la sección Bottom
    - user_permissions

frmUserResetPassword
    Formulario para actualización/reseteo de contraseñas
    - username
    - password
"""
from django import forms
from zend_django.hiperforms import HorizontalModelForm, HorizontalForm

from django.contrib.auth.models import User


class frmUser(HorizontalModelForm):
    """
    Formulario principal del modelo User

    Campos
    ------
    - username
    - password
    - first_name
    - last_name
    - apellido_materno
    - email
    - telefono
    - celular
    - whatsapp
    - is_staff
    - is_active
    - is_superuser
    - groups
    - user_permissions
    """
    apellido_materno = forms.CharField(max_length=50, required=False)
    telefono = forms.CharField(max_length=10, required=False)
    celular = forms.CharField(max_length=10, required=False)
    whatsapp = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'is_superuser',
            'groups',
            'user_permissions',
        ]
        labels = {
            'username': "Usuario",
            'password': "Contraseña",
            'first_name': "Nombre",
            'last_name': "Apellido paterno",
            'email': "EMail",
            'is_staff': "Staff",
            'is_active': "Activo",
            'is_superuser': "SuperUsuario",
            'groups': "Perfiles",
            'user_permissions': "Permisos",
        }
        widgets = {
            'groups': forms.SelectMultiple(attrs={"size":5}),
            'user_permissions': forms.SelectMultiple(attrs={"size":25}),
            'password': forms.PasswordInput(),
        }
    field_order = [
        'username',
        'password',
        'first_name',
        'last_name',
        'apellido_materno',
        'email',
        'telefono',
        'celular',
        'whatsapp',
        'is_staff',
        'is_active',
        'is_superuser',
        'groups',
        'user_permissions',
    ]


class frmUserUpdate(HorizontalModelForm):
    """
    Formulario para actualizacion de usuarios

    Campos
    ------
    - first_name
    - last_name
    - apellido_materno
    - email
    - telefono
    - celular
    - whatsapp
    - is_staff
    - is_active
    - is_superuser
    - groups
    - user_permissions
    """
    apellido_materno = forms.CharField(max_length=50, required=False)
    telefono = forms.CharField(max_length=10, required=False)
    celular = forms.CharField(max_length=10, required=False)
    whatsapp = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'is_superuser',
            'groups',
            'user_permissions',
        ]
        labels = {
            'first_name': "Nombre",
            'last_name': "Apellido paterno",
            'email': "EMail",
            'is_staff': "Staff",
            'is_active': "Activo",
            'is_superuser': "SuperUsuario",
            'groups': "Perfiles",
            'user_permissions': "Permisos",
        }
        widgets = {
            'groups': forms.SelectMultiple(attrs={"size":5}),
            'user_permissions': forms.SelectMultiple(attrs={"size":25}),
        }
    field_order = [
        'first_name',
        'last_name',
        'apellido_materno',
        'email',
        'telefono',
        'celular',
        'whatsapp',
        'is_staff',
        'is_active',
        'is_superuser',
        'groups',
        'user_permissions',
    ]


class frmUserTop(HorizontalModelForm):
    """
    Formulario para desplegado en la sección Top

    Campos
    ------
    - username
    - password
    """

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        labels = {
            'username': "Usuario",
            'password': "Contraseña",
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
    field_order = [
        'username',
        'password',
    ]


class frmUserTopMe(forms.Form):
    """
    Formulario para desplegado en la sección Top

    Campos
    ------
    - username
    - password
    """
    username = forms.CharField(
        max_length=50, label="Usuario",
        widget=forms.TextInput())
    password = forms.CharField(
        max_length=50, label="Contraseña", required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva Contraseña'}))


class frmUserTopReadUpdate(HorizontalModelForm):
    """
    Formulario para desplegado en la sección Top (Read/Update)

    Campos
    ------
    - username
    """

    class Meta:
        model = User
        fields = [
            'username',
        ]
        labels = {
            'username': "Usuario",
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
    field_order = [
        'username',
    ]


class frmUserLeft(HorizontalModelForm):
    """
    Formulario para desplegado en la sección Left

    Campos
    ------
    - first_name
    - last_name
    - apellido_materno
    - email
    - telefono
    - celular
    - whatsapp
    """
    apellido_materno = forms.CharField(max_length=50, required=False)
    telefono = forms.CharField(max_length=10, required=False)
    celular = forms.CharField(max_length=10, required=False)
    whatsapp = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'first_name': "Nombre",
            'last_name': "Apellido paterno",
            'email': "EMail",
        }
    field_order = [
        'first_name',
        'last_name',
        'apellido_materno',
        'email',
        'telefono',
        'celular',
        'whatsapp',
    ]


class frmUserRight(HorizontalModelForm):
    """
    Formulario para desplegado en la sección Right

    Campos
    ------
    - is_staff
    - is_active
    - is_superuser
    - groups
    """

    class Meta:
        model = User
        fields = [
            'is_staff',
            'is_active',
            'is_superuser',
            'groups',
        ]
        labels = {
            'is_staff': "Staff",
            'is_active': "Activo",
            'is_superuser': "SuperUsuario",
            'groups': "Perfiles",
        }
        widgets = {
            'groups': forms.SelectMultiple(attrs={"size":5}),
        }
    field_order = [
        'is_staff',
        'is_active',
        'is_superuser',
        'groups',
    ]


class frmUserBottom(HorizontalModelForm):
    """
    Formulario para desplegado en la sección Bottom

    Campos
    ------
    - user_permissions
    """

    class Meta:
        model = User
        fields = [
            'user_permissions',
        ]
        labels = {
            'user_permissions': "Permisos",
        }
        widgets = {
            'user_permissions': forms.SelectMultiple(attrs={"size":25}),
        }
    field_order = [
        'user_permissions',
    ]


class frmUserResetPassword(HorizontalForm):
    """
    Formulario para actualización/reseteo de contraseñas

    Campos
    ------
    - username
    - password
    """
    username = forms.CharField(required=True, max_length=50, label="Usuario")
    password = forms.CharField(
        required=True, max_length=50,
        label="Contraseña", widget=forms.PasswordInput())
