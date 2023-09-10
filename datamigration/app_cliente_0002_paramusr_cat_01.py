from zend_django.models import ParametroUsuario

def migration():
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="estatusactividad")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="medioactividad")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="tipoactividad")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="tipodocumento")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="taxonomiaexpediente")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="recursoexterno")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="uma")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="cuantiabasica")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="factoredad")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="bootstrapcolor")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="estadocivil")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="estatuspago")
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="cuentapago")
    