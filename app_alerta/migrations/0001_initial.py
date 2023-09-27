# Generated by Django 4.1.3 on 2023-09-27 17:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Alerta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nota", models.TextField()),
                ("fecha_alerta", models.DateField(default=datetime.date.today)),
                ("alertado", models.BooleanField(default=False)),
                ("fecha_alertado", models.DateField(blank=True, null=True)),
                ("mostrar_alerta", models.BooleanField(default=True)),
                ("fecha_no_mostrar", models.DateField(blank=True, null=True)),
                ("creado_por", models.TextField(blank=True, max_length=250)),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("actualizado_por", models.TextField(blank=True, max_length=250)),
                ("fecha_actualizacion", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="alertas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-fecha_alerta", "-actualizado_por", "-creado_por"],
                "permissions": [
                    ("get_alerta", "Obtener mis alertas"),
                    ("disabled_alerta", "Desactivar alerta"),
                ],
            },
        ),
    ]