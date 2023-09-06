from django.db import models


class Direccion(models.Model):
    calle = models.CharField(max_length=100, blank=True)
    numero_exterior = models.CharField(
        max_length=10,
        verbose_name="No. Exterior",
        blank=True)
    numero_interior = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="No. Interior")
    codigo_postal = models.CharField(max_length=5, blank=True)
    colonia = models.CharField(max_length=100, blank=True)
    municipio = models.CharField(
        max_length=100,
        verbose_name="Alcaldía o Municipio",
        blank=True)
    estado = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.asDireccion()[0]

    def __unicode__(self):
        return self.asDireccion()[0]

    def asDireccion(self):
        return (
            "{} {}{},<br />{}, {},<br />{},<br />"
            "C.P. {}").format(
                self.calle, self.numero_exterior,
                " (Int. {})".format(
                    self.numero_interior) if self.numero_interior else "",
                self.colonia, self.municipio, self.estado,
                self.codigo_postal)
