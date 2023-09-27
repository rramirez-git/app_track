import pandas as pd

from datetime import date
from django.db import models

from app_catalogo.models import EstadoCivil
from app_catalogo.models import TaxonomiaExpediente
from app_cliente.models import Direccion
from zend_django.models import UserProfile


def UserProfilePkCliente():
    try:
        return [cte.userprofile.pk for cte in Cliente.objects.all()]
    except NameError:
        print("*********************** NO EXISTE ***********************")
        return list()


def UserProfilePkNoCliente():
    dfUsr = pd.DataFrame(
        list(usrp.pk for usrp in UserProfile.objects.all()),
        columns=['pk'])
    return dfUsr[~dfUsr.pk.isin(UserProfilePkCliente())]['pk'].to_list()


def UserProfileResponsables():
    resps = list()
    for pk in UserProfilePkNoCliente():
        usrp = UserProfile.objects.filter(pk=pk)[0]
        resps.append((usrp.pk, f"{usrp}"), )
    return resps


class Cliente(models.Model):
    userprofile = models.OneToOneField(
        to=UserProfile, on_delete=models.CASCADE, related_name="profile")
    contraseña = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de nacimiento", blank=True, default=date.today)
    CURP = models.CharField(max_length=18, blank=True)
    RFC = models.CharField(max_length=13, blank=True)
    NSS = models.CharField(max_length=15, blank=True)
    estado_civil = models.ForeignKey(
        to=EstadoCivil,
        on_delete=models.RESTRICT,
        related_name="+")
    conyuge = models.CharField(max_length=150, blank=True)
    clinica = models.CharField(
        max_length=150, blank=True, verbose_name="Clínica")
    subdelegacion = models.CharField(
        max_length=150, blank=True, verbose_name="Subdelegación")
    empresa = models.CharField(max_length=150, blank=True)
    domicilio = models.ForeignKey(
        Direccion, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="cliente")
    telefono_oficina = models.CharField(
        max_length=10, blank=True, verbose_name="Teléfono de oficina")
    otro_telefono = models.CharField(
        max_length=10, blank=True, verbose_name="Otro teléfono")
    afore_actual = models.CharField(max_length=50, blank=True)
    fecha_afore_actual = models.DateField(blank=True, default=date.today)
    tipo = models.ForeignKey(
        TaxonomiaExpediente,
        on_delete=models.PROTECT,
        related_name='clientes')
    observaciones = models.TextField(blank=True)
    obs_semanas_cotizadas = models.TextField(
        blank=True, verbose_name="Semanas Cotizadas")
    obs_homonimia = models.TextField(
        blank=True, verbose_name="Homonimia")
    obs_duplicidad = models.TextField(
        blank=True, verbose_name="Duplicidad")
    responsable = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        related_name="clientes_asignados",
        blank=True,
        null=True,
        verbose_name="Ejecutivo"
        )
    gestor = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        related_name="clientes_gestionados",
        blank=True,
        null=True
        )

    @property
    def edad(self):
        anios = date.today().year - self.fecha_nacimiento.year
        if date.today().month < self.fecha_nacimiento.month:
            anios -= 1
        elif (date.today().month == self.fecha_nacimiento.month
                and date.today().day < self.fecha_nacimiento.day):
            anios -= 1
        return anios

    class Meta:
        ordering = [
            "userprofile__user__last_name",
            "userprofile__apellido_materno",
            "userprofile__user__first_name"]
        permissions = [
            ('import_cliente', 'Importar clientes'),
        ]

    def __str__(self):
        return "{} {} {} - {}".format(
            self.userprofile.user.last_name,
            self.userprofile.apellido_materno,
            self.userprofile.user.first_name,
            self.pk,
            ).strip()

    def __unicode__(self):
        return self.__str__()
