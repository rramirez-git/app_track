from django.db import models


class TipoDocumento(models.Model):
    tipo_de_documento = models.CharField(max_length=50)
    visible_para_usuario = models.BooleanField(default=True)

    class Meta:
        ordering = ["tipo_de_documento"]

    def __str__(self):
        return self.tipo_de_documento.strip()

    def __unicode__(self):
        return self.__str__()
