from django import forms
from django.contrib.auth.models import User

from zend_django.hiperforms import HorizontalModelForm, HorizontalForm

from .models import Cliente, UserProfile
from .models import UserProfileResponsables


class frmCteUser(HorizontalModelForm):
    apellido_materno = forms.CharField(max_length=250, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
        ]
        labels = {
            'last_name': 'Apellido Paterno'
        }

    field_order = [
        'username',
        'password',
        'contraseña',
        'first_name',
        'last_name',
        'apellido_materno',
    ]


class frmCteContacto(HorizontalModelForm):
    email = forms.EmailField()
    telefono_oficina = forms.CharField(max_length=10, required=False)
    otro_telefono = forms.CharField(max_length=10, required=False)

    class Meta:
        model = UserProfile
        fields = [
            'telefono',
            'celular',
            'whatsapp',
        ]

        widgets = {
            'telefono': forms.TextInput(attrs={'type': 'tel'}),
            'celular': forms.TextInput(attrs={'type': 'tel'}),
            'whatsapp': forms.TextInput(attrs={'type': 'tel'}),
            'telefono_oficina': forms.TextInput(attrs={'type': 'tel'}),
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


class frmCteGenerales(HorizontalModelForm):
    def __init__(self, *args, **kwargs):
        super(frmCteGenerales, self).__init__(*args, **kwargs)
        self.fields['responsable'].choices = UserProfileResponsables()
        self.fields['gestor'].choices = UserProfileResponsables()

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
            'responsable',
            'gestor',
        ]
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'type': 'date'}),
            'fecha_afore_actual': forms.TextInput(attrs={'type': 'date'}),
        }

    field_order = [
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
        'responsable',
        'gestor',
    ]


class frmCteOtros(HorizontalForm):
    obs_semanas_cotizadas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows":"5"}),
        label="Semanas Cotizadas")
    obs_homonimia = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows":"5"}),
        label="Homonimia")
    obs_duplicidad = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows":"5"}),
        label="Duplicidad")
    observaciones = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows":"5"}))
    