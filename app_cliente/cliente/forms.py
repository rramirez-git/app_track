from django import forms

from zend_django.hiperforms import HorizontalModelForm

from .models import Cliente
from .models import UserProfileResponsables


class frmCliente(HorizontalModelForm):
    username = forms.CharField(max_length=250, label="Usuario")
    email = forms.EmailField()
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    apellido_materno = forms.CharField(max_length=250)
    telefono = forms.CharField(max_length=25)
    celular = forms.CharField(max_length=25)
    whatsapp = forms.CharField(max_length=25)

    class Meta:
        model = Cliente
        fields = [
            'contraseña',
            'telefono_oficina',
            'otro_telefono',
            'tipo',
            'fecha_nacimiento',
            'CURP',
            'RFC',
            'NSS',
            'estado_civil',
            'conyuge',
            'empresa',
            'afore_actual',
            'fecha_afore_actual',
            'clinica',
            'subdelegacion',
            'observaciones',
            'obs_semanas_cotizadas',
            'obs_homonimia',
            'obs_duplicidad',
            'responsable',
            'gestor',
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido Paterno',
            'email': 'E-Mail',
            'tipo': 'Tipo de Expediente',
        }
        widgets = {
            'telefono': forms.TextInput(attrs={'type': 'tel'}),
            'celular': forms.TextInput(attrs={'type': 'tel'}),
            'telefono_oficina': forms.TextInput(attrs={'type': 'tel'}),
            'otro_telefono': forms.TextInput(attrs={'type': 'tel'}),
            'fecha_nacimiento': forms.TextInput(attrs={'type': 'date'}),
            'fecha_afore_actual': forms.TextInput(attrs={'type': 'date'}),
        }

    field_order = [
            'username',
            'contraseña',
            'email',
            'first_name',
            'last_name',
            'apellido_materno',
            'telefono',
            'celular',
            'whatsapp',
            'telefono_oficina',
            'otro_telefono',
            'tipo',
            'fecha_nacimiento',
            'CURP',
            'RFC',
            'NSS',
            'estado_civil',
            'conyuge',
            'empresa',
            'afore_actual',
            'fecha_afore_actual',
            'clinica',
            'subdelegacion',
            'observaciones',
            'obs_semanas_cotizadas',
            'obs_homonimia',
            'obs_duplicidad',
            'responsable',
            'gestor',
        ]


class frmClienteUsuario(HorizontalModelForm):
    username = forms.CharField(max_length=250, label="Usuario")
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    apellido_materno = forms.CharField(max_length=250)

    class Meta:
        model = Cliente
        fields = [
            'username',
            'contraseña',
            'first_name',
            'last_name',
            'apellido_materno',
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido Paterno',
        }

    field_order = [
            'username',
            'contraseña',
            'first_name',
            'last_name',
            'apellido_materno',
        ]


class frmClienteContacto(HorizontalModelForm):
    email = forms.EmailField()
    telefono = forms.CharField(max_length=25)
    celular = forms.CharField(max_length=25)
    whatsapp = forms.CharField(max_length=25)

    class Meta:
        model = Cliente
        fields = [
            'telefono_oficina',
            'otro_telefono',
        ]
        labels = {
            'email': 'E-Mail',
        }
        widgets = {
            'telefono': forms.TextInput(attrs={'type': 'tel'}),
            'celular': forms.TextInput(attrs={'type': 'tel'}),
            'telefono_oficina': forms.TextInput(attrs={'type': 'tel'}),
            'whatsapp': forms.TextInput(attrs={'type': 'tel'}),
            'otro_telefono': forms.TextInput(attrs={'type': 'tel'}),
        }

    field_order = [
            'email',
            'telefono',
            'celular',
            'whatsapp',
            'telefono_oficina',
            'otro_telefono',
        ]


class frmClienteTrabajo(HorizontalModelForm):

    class Meta:
        model = Cliente
        fields = [
            'tipo',
            'fecha_nacimiento',
            'CURP',
            'RFC',
            'NSS',
            'estado_civil',
            'conyuge',
            'empresa',
            'afore_actual',
            'fecha_afore_actual',
            'clinica',
            'subdelegacion',
        ]
        labels = {
            'tipo': 'Tipo de Expediente',
        }
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'type': 'date'}),
            'fecha_afore_actual': forms.TextInput(attrs={'type': 'date'}),
        }


class frmClienteObservaciones(HorizontalModelForm):

    class Meta:
        model = Cliente
        fields = ['observaciones']


class frmClienteOtro(HorizontalModelForm):
    responsable = forms.ChoiceField(
        required=False, choices=UserProfileResponsables, label="Ejecutivo")
    gestor = forms.ChoiceField(
        required=False, choices=UserProfileResponsables, label="Gestor")

    class Meta:
        model = Cliente
        fields = [
            'obs_semanas_cotizadas',
            'obs_homonimia',
            'obs_duplicidad',
        ]
