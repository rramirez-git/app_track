from django.db import models


class CuantiaBasica(models.Model):
    salario_inicio = models.DecimalField(max_digits=6, decimal_places=4)
    salario_fin = models.DecimalField(max_digits=6, decimal_places=4)
    porcentaje_de_cuantia_basica = models.DecimalField(
        max_digits=5, decimal_places=3)
    porcentaje_de_incremento_anual = models.DecimalField(
        max_digits=5, decimal_places=3)

    class Meta:
        ordering = ['salario_inicio', 'salario_fin']

    def __str__(self):
        return f"de {self.salario_inicio} a {self.salario_fin}"

    def __unicode__(self):
        return self.__str__()
