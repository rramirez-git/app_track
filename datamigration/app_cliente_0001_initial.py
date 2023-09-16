from django.contrib.auth.models import Permission, Group

from app_catalogo.models import BootstrapColor
from app_catalogo.models import BootstrapColor
from app_catalogo.models import CuantiaBasica
from app_catalogo.models import CuentaPago
from app_catalogo.models import EstadoCivil
from app_catalogo.models import EstatusActividad
from app_catalogo.models import EstatusPago
from app_catalogo.models import FactorEdad
from app_catalogo.models import MedioActividad
from app_catalogo.models import RecursoExterno
from app_catalogo.models import TaxonomiaExpediente
from app_catalogo.models import TipoActividad
from app_catalogo.models import TipoDocumento
from app_catalogo.models import UMA
from zend_django.models import MenuOpc, ParametroUsuario
from app_catalogo.models import TipoParametro

from .utils import update_permisos


def migration():
    update_permisos()

    Group.objects.get_or_create(name="Cliente")
    Group.objects.get_or_create(name="Comercial")

    app = MenuOpc.objects.get_or_create(
        nombre="Clientes", posicion=50, vista='idx_app_cliente')[0]
    opc = MenuOpc.objects.get_or_create(
        nombre="Clientes",
        vista="cliente_list",
        posicion=1,
        padre=app
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_cliente'),
        Permission.objects.get(codename='change_cliente'),
        Permission.objects.get(codename='delete_cliente'),
        Permission.objects.get(codename='view_cliente'),
    ])

    cat = MenuOpc.objects.get_or_create(
        nombre="Catalogos", posicion=75, vista='idx_app_catalogo')[0]

    opc = MenuOpc.objects.get_or_create(
        nombre="Estatus Actividad",
        vista="estatusactividad_list",
        posicion=1,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_estatusactividad'),
        Permission.objects.get(codename='change_estatusactividad'),
        Permission.objects.get(codename='delete_estatusactividad'),
        Permission.objects.get(codename='view_estatusactividad'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Medios de Actividad",
        vista="medioactividad_list",
        posicion=2,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_medioactividad'),
        Permission.objects.get(codename='change_medioactividad'),
        Permission.objects.get(codename='delete_medioactividad'),
        Permission.objects.get(codename='view_medioactividad'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Tipos de Actividad",
        vista="tipoactividad_list",
        posicion=3,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_tipoactividad'),
        Permission.objects.get(codename='change_tipoactividad'),
        Permission.objects.get(codename='delete_tipoactividad'),
        Permission.objects.get(codename='view_tipoactividad'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Tipos de Documento",
        vista="tipodocumento_list",
        posicion=4,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_tipodocumento'),
        Permission.objects.get(codename='change_tipodocumento'),
        Permission.objects.get(codename='delete_tipodocumento'),
        Permission.objects.get(codename='view_tipodocumento'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Tipos de Expediente",
        vista="taxonomiaexpediente_list",
        posicion=5,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_taxonomiaexpediente'),
        Permission.objects.get(codename='change_taxonomiaexpediente'),
        Permission.objects.get(codename='delete_taxonomiaexpediente'),
        Permission.objects.get(codename='view_taxonomiaexpediente'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Personas Externas",
        vista="recursoexterno_list",
        posicion=6,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_recursoexterno'),
        Permission.objects.get(codename='change_recursoexterno'),
        Permission.objects.get(codename='delete_recursoexterno'),
        Permission.objects.get(codename='view_cuantiabasica'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Unidad de Medida y Actualización (UMA)",
        vista="uma_list",
        posicion=7,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_uma'),
        Permission.objects.get(codename='change_uma'),
        Permission.objects.get(codename='delete_uma'),
        Permission.objects.get(codename='view_uma'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Cuantía Básica e Incremento Anual",
        vista="cuantiabasica_list",
        posicion=8,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_cuantiabasica'),
        Permission.objects.get(codename='change_cuantiabasica'),
        Permission.objects.get(codename='delete_cuantiabasica'),
        Permission.objects.get(codename='view_cuantiabasica'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Porcentaje de Factor de Edad",
        vista="factoredad_list",
        posicion=9,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_factoredad'),
        Permission.objects.get(codename='change_factoredad'),
        Permission.objects.get(codename='delete_factoredad'),
        Permission.objects.get(codename='view_factoredad'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Colores Bootstrap",
        vista="bootstrapcolor_list",
        posicion=100,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_bootstrapcolor'),
        Permission.objects.get(codename='change_bootstrapcolor'),
        Permission.objects.get(codename='delete_bootstrapcolor'),
        Permission.objects.get(codename='view_bootstrapcolor'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Estado Civil",
        vista="estadocivil_list",
        posicion=102,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_estadocivil'),
        Permission.objects.get(codename='change_estadocivil'),
        Permission.objects.get(codename='delete_estadocivil'),
        Permission.objects.get(codename='view_estadocivil'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Estatus de Pago",
        vista="estatuspago_list",
        posicion=103,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_estatuspago'),
        Permission.objects.get(codename='change_estatuspago'),
        Permission.objects.get(codename='delete_estatuspago'),
        Permission.objects.get(codename='view_estatuspago'),
    ])

    opc = MenuOpc.objects.get_or_create(
        nombre="Cuentas de Pago",
        vista="cuentapago_list",
        posicion=104,
        padre=cat
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_cuentapago'),
        Permission.objects.get(codename='change_cuentapago'),
        Permission.objects.get(codename='delete_cuentapago'),
        Permission.objects.get(codename='view_cuentapago'),
    ])

    bcNinguno = BootstrapColor.objects.get_or_create(
        nombre='Ninguno', clase_color='')[0]
    bcPrimary = BootstrapColor.objects.get_or_create(
        nombre='Primary', clase_color='primary')[0]
    bcSecondary = BootstrapColor.objects.get_or_create(
        nombre='Secondary', clase_color='secondary')[0]
    bcSuccess = BootstrapColor.objects.get_or_create(
        nombre='Success', clase_color='success')[0]
    bcDanger = BootstrapColor.objects.get_or_create(
        nombre='Danger', clase_color='danger')[0]
    bcWarning = BootstrapColor.objects.get_or_create(
        nombre='Warning', clase_color='warning')[0]
    bcInfo = BootstrapColor.objects.get_or_create(
        nombre='Info', clase_color='info')[0]
    bcLight = BootstrapColor.objects.get_or_create(
        nombre='Light', clase_color='light')[0]
    bcDark = BootstrapColor.objects.get_or_create(
        nombre='Dark', clase_color='dark')[0]

    EstatusActividad.objects.get_or_create(
        estatus_de_la_actividad='01 PENDIENTE',
        color=bcPrimary, mostrar_en_panel=True)
    EstatusActividad.objects.get_or_create(
        estatus_de_la_actividad='02 EN PROCESO',
        color=bcSuccess, mostrar_en_panel=True)
    EstatusActividad.objects.get_or_create(
        estatus_de_la_actividad='03 CONCLUIDA',
        color=bcSecondary, mostrar_en_panel=False)

    MedioActividad.objects.get_or_create(medio='Internet')
    MedioActividad.objects.get_or_create(medio='Arturo')
    MedioActividad.objects.get_or_create(medio='Michael')
    MedioActividad.objects.get_or_create(medio='Ventanilla')
    MedioActividad.objects.get_or_create(medio='Otro')
    MedioActividad.objects.get_or_create(medio='000000')

    TipoActividad.objects.get_or_create(
        tipo_de_actividad='CORRECCION IMSS')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='CORRECCION RENAPO')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='CORRECCION AFORE')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='TRASPASO AFORE')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='ALTA MOD 40')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='BAJA MOD 40')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='INCONFORMIDAD')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='RETIRO TOTAL')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='ESTUDIO')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='COBRO TOTAL')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='CORRECCION PRORROGAS')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='ANTICIPOS MENSUALES')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='ANTICIPO(S)')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='COBRANZA')
    TipoActividad.objects.get_or_create(
        tipo_de_actividad='BVo PENSION CONCLUIDA')

    TipoDocumento.objects.get_or_create(
        tipo_de_documento='ACTA NACIMIENTO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CURP',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='IDENTIFICACION OFICIAL',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='RFC',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='NSS',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='ESTADO CUENTA AFORE',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CERTIFICADO CORRECCION DATOS',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CARTA INSCRIPCION MOD 40',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CERTIFICADO DE DERECHOS',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='SEMANAS COTIZADAS',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='COMPROBANTE DOMICILIO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='ACTA NACIMIENTO ESPOSA',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='ACTA MATRIMONIO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CURP ESPOSA',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='IDENTIFICACION OFICIAL ESPOSA',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CONTRATO BANCO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='ESTADO CUENTA BANCO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CARTA BAJA MOD 40',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='APORTACIONES INFONAVIT',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='HOJA ROSA',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='OTRO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='PODER NOTARIAL',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='DOCUMENTO ELECCION REGIMEN',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='RESOLUCION PENSION',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='SOLICITUD PENSION',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='Estudio',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='REGISTRO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CONTRATO SERVICIO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='ALFANUMERICO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='INCONFORMIDAD',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='ALTA PATRON SUSTITUTO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='BAJA PATRON SUSTITUTO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CARNET',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='PAGO MOD 40',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='PROYECTO PENSION',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CONSTANCIA VIGENCIA BENEFICIARIOS',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='CREDENCIAL ADIMSS',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='LINEA CAPTURA PAGO MOD 40',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='SINAVID',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='ALTA MOD 40',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='BAJA MOD 40',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='COMPROBANTE PAGO/ANTICIPO',
        visible_para_usuario=True)
    TipoDocumento.objects.get_or_create(
        tipo_de_documento='PAGO/ANTICIPO',
        visible_para_usuario=True)

    TaxonomiaExpediente.objects.get_or_create(
        nombre="01 RECEPCION",
        color=bcPrimary, mostrar_en_panel=True)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="02 CARTERA EN ESPERA",
        color=bcInfo, mostrar_en_panel=False)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="03 MOD 40 PROXIMOS",
        color=bcWarning, mostrar_en_panel=True)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="04 MOD 40 INSCRITOS",
        color=bcWarning, mostrar_en_panel=False)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="05 PATRON SUSTITUTO",
        color=bcWarning, mostrar_en_panel=False)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="06 REACTIVACION",
        color=bcNinguno, mostrar_en_panel=False)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="07 PENSIONES PROXIMAS",
        color=bcDanger, mostrar_en_panel=True)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="08 PENSIONES EN PROCESO",
        color=bcSuccess, mostrar_en_panel=True)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="09 PENSIONES CONCLUIDAS",
        color=bcDark, mostrar_en_panel=False)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="10 PROYECTO DE PENSION",
        color=bcNinguno, mostrar_en_panel=False)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="11 ASISTENCIA VIUDEZ",
        color=bcNinguno, mostrar_en_panel=False)
    TaxonomiaExpediente.objects.get_or_create(
        nombre="12 OTRO ESTATUS",
        color=bcSecondary, mostrar_en_panel=False)

    RecursoExterno.objects.get_or_create(
        nombre='artur', apellido_paterno='', apellido_materno='')
    RecursoExterno.objects.get_or_create(
        nombre='rebeca', apellido_paterno='', apellido_materno='')
    RecursoExterno.objects.get_or_create(
        nombre='nancy areli', apellido_paterno='', apellido_materno='')
    RecursoExterno.objects.get_or_create(
        nombre='mario alberto', apellido_paterno='', apellido_materno='')
    RecursoExterno.objects.get_or_create(
        nombre='josé martín', apellido_paterno='', apellido_materno='')
    RecursoExterno.objects.get_or_create(
        nombre='daniel', apellido_paterno='', apellido_materno='')
    RecursoExterno.objects.get_or_create(
        nombre='josé alfredo', apellido_paterno='', apellido_materno='')
    RecursoExterno.objects.get_or_create(
        nombre='karen', apellido_paterno='', apellido_materno='')
    RecursoExterno.objects.get_or_create(
        nombre='socorro', apellido_paterno='', apellido_materno='')
    RecursoExterno.objects.get_or_create(
        nombre='jenifer', apellido_paterno='', apellido_materno='')

    UMA.objects.get_or_create(año=2016, valor=73.04)
    UMA.objects.get_or_create(año=2017, valor=75.49)
    UMA.objects.get_or_create(año=2018, valor=80.6)
    UMA.objects.get_or_create(año=2019, valor=84.49)
    UMA.objects.get_or_create(año=2020, valor=86.88)
    UMA.objects.get_or_create(año=2021, valor=89.62)
    UMA.objects.get_or_create(año=2022, valor=96.22)
    UMA.objects.get_or_create(año=2023, valor=103.74)

    CuantiaBasica.objects.get_or_create(
        salario_inicio=0, salario_fin=1,
        porcentaje_de_cuantia_basica=80,
        porcentaje_de_incremento_anual=0.563)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=1.0001, salario_fin=1.25,
        porcentaje_de_cuantia_basica=77.11,
        porcentaje_de_incremento_anual=0.814)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=1.2501, salario_fin=1.5,
        porcentaje_de_cuantia_basica=58.18,
        porcentaje_de_incremento_anual=1.178)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=1.5001, salario_fin=1.75,
        porcentaje_de_cuantia_basica=49.23,
        porcentaje_de_incremento_anual=1.43)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=1.7501, salario_fin=2,
        porcentaje_de_cuantia_basica=42.67,
        porcentaje_de_incremento_anual=1.615)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=2.0001, salario_fin=2.25,
        porcentaje_de_cuantia_basica=37.65,
        porcentaje_de_incremento_anual=1.756)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=2.2501, salario_fin=2.5,
        porcentaje_de_cuantia_basica=33.68,
        porcentaje_de_incremento_anual=1.868)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=2.5001, salario_fin=2.75,
        porcentaje_de_cuantia_basica=30.48,
        porcentaje_de_incremento_anual=1.958)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=2.7501, salario_fin=3,
        porcentaje_de_cuantia_basica=27.83,
        porcentaje_de_incremento_anual=2.033)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=3.0001, salario_fin=3.25,
        porcentaje_de_cuantia_basica=25.6,
        porcentaje_de_incremento_anual=2.096)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=3.2501, salario_fin=3.5,
        porcentaje_de_cuantia_basica=23.7,
        porcentaje_de_incremento_anual=2.149)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=3.5001, salario_fin=3.75,
        porcentaje_de_cuantia_basica=22.07,
        porcentaje_de_incremento_anual=2.195)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=3.7501, salario_fin=4,
        porcentaje_de_cuantia_basica=20.65,
        porcentaje_de_incremento_anual=2.235)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=4.0001, salario_fin=4.25,
        porcentaje_de_cuantia_basica=19.39,
        porcentaje_de_incremento_anual=2.271)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=4.2501, salario_fin=4.5,
        porcentaje_de_cuantia_basica=18.29,
        porcentaje_de_incremento_anual=2.302)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=4.5001, salario_fin=4.75,
        porcentaje_de_cuantia_basica=17.3,
        porcentaje_de_incremento_anual=2.33)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=4.7501, salario_fin=5,
        porcentaje_de_cuantia_basica=16.41,
        porcentaje_de_incremento_anual=2.355)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=5.0001, salario_fin=5.25,
        porcentaje_de_cuantia_basica=15.61,
        porcentaje_de_incremento_anual=2.377)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=5.2501, salario_fin=5.5,
        porcentaje_de_cuantia_basica=14.88,
        porcentaje_de_incremento_anual=2.398)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=5.5001, salario_fin=5.75,
        porcentaje_de_cuantia_basica=14.22,
        porcentaje_de_incremento_anual=2.416)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=5.7501, salario_fin=6,
        porcentaje_de_cuantia_basica=13.62,
        porcentaje_de_incremento_anual=2.433)
    CuantiaBasica.objects.get_or_create(
        salario_inicio=6.0001, salario_fin=99.9999,
        porcentaje_de_cuantia_basica=13,
        porcentaje_de_incremento_anual=2.45)

    FactorEdad.objects.get_or_create(edad=60, factor_de_edad=75)
    FactorEdad.objects.get_or_create(edad=61, factor_de_edad=80)
    FactorEdad.objects.get_or_create(edad=62, factor_de_edad=85)
    FactorEdad.objects.get_or_create(edad=63, factor_de_edad=90)
    FactorEdad.objects.get_or_create(edad=64, factor_de_edad=95)
    FactorEdad.objects.get_or_create(edad=65, factor_de_edad=100)

    EstadoCivil.objects.get_or_create(estado_civil="Soltero")
    EstadoCivil.objects.get_or_create(estado_civil="Casado")
    EstadoCivil.objects.get_or_create(estado_civil="Unión Libre")
    EstadoCivil.objects.get_or_create(estado_civil="Separado")
    EstadoCivil.objects.get_or_create(estado_civil="Divorciado")
    EstadoCivil.objects.get_or_create(estado_civil="Viudo")

    EstatusPago.objects.get_or_create(estatus_de_pago='Pendiente de Pago')
    EstatusPago.objects.get_or_create(estatus_de_pago='Pagado')
    EstatusPago.objects.get_or_create(estatus_de_pago='Pagado y Verificado')

    CuentaPago.objects.get_or_create(cuenta_de_pago='Efectivo')
    CuentaPago.objects.get_or_create(cuenta_de_pago='Daniel Azteca')
    CuentaPago.objects.get_or_create(cuenta_de_pago='Daniel Banamex')
    CuentaPago.objects.get_or_create(cuenta_de_pago='Sosa del Bosque')

    tpCadena = TipoParametro.objects.get_or_create(
        nombre="Cadena", tipo_interno="STRING")[0]
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="estatusactividad", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="medioactividad", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="tipoactividad", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="tipodocumento", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="taxonomiaexpediente", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="recursoexterno", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="uma", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="cuantiabasica", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="factoredad", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="bootstrapcolor", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="estadocivil", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="estatuspago", tipo=tpCadena)
    ParametroUsuario.objects.get_or_create(
        seccion="basic_search", nombre="cuentapago", tipo=tpCadena)