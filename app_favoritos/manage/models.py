"""
Definición de modelos de Favorito (administración general)

Modelos
-------
- Favorito
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Favorito(models.Model):
    """
    Modelo de Favorito (administración general)
    """
    usuario = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='mis_favoritos')
    etiqueta = models.CharField(max_length=300)
    url = models.URLField(max_length=500)

    class Meta:
        ordering = ['usuario', 'etiqueta', 'url']
        permissions = [
            ('view_mine_fav', 'Ver Mis Favoritos'),
            ('add_mine_fav', 'Agregar Mis Favoritos'),
            ('change_mine_fav', 'Actualizar Mis Favoritos'),
            ('delete_mine_fav', 'Eliminar Mis Favoritos'),
        ]
        unique_together = [
            ['usuario', 'url']
        ]

    @property
    def strAsInternal(self) -> str:
        return f'<a  href="{self.url}" class="fav-lnk">{self.etiqueta}</a>'

    @property
    def strAsExternal(self) -> str:
        att = f'href="{self.url}" class="fav-lnk" target="_blank"'
        return f'<a {att}>{self.etiqueta}</a>'

    @property
    def isInternal(self) -> bool:
        for host in settings.ALLOWED_HOSTS:
            if host in self.url:
                return True
        return False

    def __str__(self):
        return self.strAsInternal if self.isInternal else self.strAsExternal
