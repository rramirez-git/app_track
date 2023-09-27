from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from app_alerta.models import Alerta
from app_catalogo.models import EstadoCivil
from app_catalogo.models import TaxonomiaExpediente
from app_cliente.models import Cliente
from app_cliente.models import Direccion
from app_nota.models import Nota
from routines.utils import JsonRequest
from zend_django.models import UserProfile


class ImportCte():

    def __init__(self, inicio, fin, url) -> None:
        self.inicio = inicio
        self.fin = fin
        self.url = url + "sql2json/"
        self.responsables = dict()
        self.created_responsables = list()

    def run(self):
        resultados = {
            'inicio': self.inicio,
            'fin': self.fin,
            'url': self.url,
            'ctes': list()}
        self.check_and_load_responsables()
        clientes = self.get_clientes()
        gpo = Group.objects.get(name="Cliente")
        for id_cte in range(self.inicio, self.fin + 1):
            if id_cte in clientes.keys():
                cliente = clientes[id_cte]
                if Cliente.objects.filter(pk=cliente['idcliente']).exists():
                    resultados['ctes'].append({
                        'id': id_cte,
                        'res': 'El cliente ya existe en el sitio destino',
                        'type': 'danger', })
                    continue
                userprofile_db = self.get_or_create_user_profile(
                    cliente['username'], cliente['contraseña'],
                    cliente['first_name'], cliente['last_name'],
                    cliente['email'], cliente['is_staff'],
                    cliente['is_active'], cliente['is_superuser'],
                    cliente['apellido_materno'], cliente['telefono'],
                    cliente['celular'], cliente['celular'],
                    (gpo, ))
                cliente_db = Cliente.objects.create(
                    pk=id_cte,
                    userprofile=userprofile_db,
                    contraseña=cliente['contraseña'],
                    fecha_nacimiento=cliente['fecha_nacimiento'],
                    CURP=cliente['CURP'],
                    RFC=cliente['RFC'],
                    NSS=cliente['NSS'],
                    estado_civil=EstadoCivil.objects.get(
                        estado_civil__iexact=cliente['estado_civil']),
                    conyuge=cliente['conyuge'],
                    clinica=cliente['clinica'],
                    subdelegacion=cliente['subdelegacion'],
                    empresa=cliente['empresa'],
                    domicilio=Direccion.objects.create(
                        calle=cliente['calle'],
                        numero_exterior=cliente['numero_exterior'],
                        numero_interior=cliente['numero_interior'],
                        codigo_postal=cliente['codigo_postal'],
                        colonia=cliente['colonia'],
                        municipio=cliente['municipio'],
                        estado=cliente['estado']),
                    telefono_oficina=cliente['telefono_oficina'],
                    otro_telefono=cliente['otro_telefono'],
                    afore_actual=cliente['afore_actual'],
                    fecha_afore_actual=cliente['fecha_afore_actual'],
                    tipo=TaxonomiaExpediente.objects.get(
                        nombre__iexact=cliente['tipo']),
                    observaciones=cliente['observaciones'],
                    obs_semanas_cotizadas=cliente['obs_semanas_cotizadas'],
                    obs_homonimia=cliente['obs_homonimia'],
                    obs_duplicidad=cliente['obs_duplicidad'],
                    responsable=self.responsables[
                        cliente['responsable_username']],
                    gestor=self.responsables[cliente['gestor_username']]
                    )
                self.import_notas(
                    cliente['username'], cliente_db.userprofile.user)
                self.import_alertas(
                    cliente['username'], cliente_db.userprofile.user)
                resultados['ctes'].append({
                    'id': id_cte,
                    'res': f'Cliente agregado correctamente: {cliente_db}',
                    'type': 'success', })
            else:
                resultados['ctes'].append({
                    'id': id_cte,
                    'res': 'No existe el cliente en el sitio origen',
                    'type': 'secondary', })
        return resultados

    def check_and_load_responsables(self):
        sql = """
            select *
            from initsys_usr usr
            inner join auth_user user on usr.user_ptr_id = user.id
            left join app_cliente cte on cte.usr_ptr_id = usr.idusuario
            where cte.usr_ptr_id is null
            """.strip()
        data = JsonRequest(self.url, {'getrows': 'yes', 'sql': sql})
        gpo = Group.objects.get(name="Administrador")
        self.responsables = dict()
        for resp in data:
            username = resp['username']
            self.responsables[username] = self.get_or_create_user_profile(
                username, resp['contraseña'], resp['first_name'],
                resp['last_name'], resp['email'], resp['is_staff'],
                resp['is_active'], resp['is_superuser'],
                resp['apellido_materno'], resp['telefono'],
                resp['celular'], resp['celular'], (gpo, ))
        for username in self.created_responsables:
            self.import_notas(username, self.responsables[username].user)
            self.import_alertas(username, self.responsables[username].user)

    def get_or_create_user_profile(
            self,  username, contraseña, first_name, last_name, email,
            is_staff, is_active, is_superuser, apellido_materno, telefono,
            celular, whatsapp, grupos):
        if not UserProfile.objects.filter(
                user__username=username).exists():
            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_staff=is_staff,
                is_active=is_active,
                is_superuser=is_superuser
            )
            user.set_password(contraseña)
            for gpo in grupos:
                user.groups.add(gpo)
            userprofile = UserProfile.objects.create(
                user=user,
                apellido_materno=apellido_materno,
                telefono=telefono,
                celular=celular,
                whatsapp=whatsapp
            )
            user.save()
            userprofile.save()
            self.created_responsables.append(username)
            return userprofile
        return UserProfile.objects.get(user__username=username)

    def get_clientes(self):
        sql = f"""
            select
                cte.usr_ptr_id as usr_ptr_id,
                cte.idcliente as idcliente,
                cte.fecha_nacimiento as fecha_nacimiento,
                cte.CURP as CURP,
                cte.RFC as RFC,
                cte.NSS as NSS,
                cte.estado_civil as estado_civil,
                cte.empresa as empresa,
                cte.telefono_oficina as telefono_oficina,
                cte.otro_telefono as otro_telefono,
                cte.afore_actual as afore_actual,
                cte.fecha_afore_actual as fecha_afore_actual,
                cte.domicilicio_id as domicilicio_id,
                tipo_exp.nombre as tipo,
                cte.clinica as clinica,
                cte.conyuge as conyuge,
                cte.subdelegacion as subdelegacion,
                cte.observaciones as observaciones,
                cte.obs_duplicidad as obs_duplicidad,
                cte.obs_homonimia as obs_homonimia,
                cte.obs_semanas_cotizadas as obs_semanas_cotizadas,
                cte.gestor_id as gestor_id,
                cte.responsable_id as responsable_id,
                usr.user_ptr_id as user_ptr_id,
                usr.idusuario as idusuario,
                usr.usuario as usuario,
                usr.contraseña as contraseña,
                usr.apellido_materno as apellido_materno,
                usr.telefono as telefono,
                usr.celular as celular,
                user.id as id,
                user.password as password,
                user.last_login as last_login,
                user.is_superuser as is_superuser,
                user.username as username,
                user.first_name as first_name,
                user.email as email,
                user.is_staff as is_staff,
                user.is_active as is_active,
                user.date_joined as date_joined,
                user.last_name as last_name,
                dir.iddireccion as iddireccion,
                dir.calle as calle,
                dir.numero_interior as numero_interior,
                dir.codigo_postal as codigo_postal,
                dir.colonia as colonia,
                dir.municipio as municipio,
                dir.estado as estado,
                dir.numero_exterior as numero_exterior,
                gestor_user.username as gestor_username,
                responsable_user.username as responsable_username
            from app_cliente cte
            inner join initsys_usr usr
                on cte.usr_ptr_id = usr.idusuario
            inner join auth_user user
                on usr.user_ptr_id = user.id
            inner join initsys_direccion dir
                on cte.domicilicio_id = dir.iddireccion
            inner join initsys_usr gestor_usr
                on cte.gestor_id = gestor_usr.idusuario
            inner join auth_user gestor_user
                on gestor_usr.user_ptr_id = gestor_user.id
            inner join initsys_usr responsable_usr
                on cte.responsable_id = responsable_usr.idusuario
            inner join auth_user responsable_user
                on responsable_usr.user_ptr_id = responsable_user.id
            inner join app_taxonomiaexpediente tipo_exp
                on cte.tipo_id = tipo_exp.idtaxonomia
            where idcliente between {self.inicio} and {self.fin};
            """.strip()
        ctes = JsonRequest(self.url, {'getrows': 'yes', 'sql': sql})
        resultado = dict()
        for cte in ctes:
            resultado[cte['idcliente']] = cte
        return resultado

    def create_nota(self, reg):
        f_creacion = datetime.strftime(
            datetime.strptime(reg['created_at'], '%Y-%m-%dT%H:%M:%S.%f'),
            '%d/%m/%Y %H:%M:%S')
        f_actualizacion = datetime.strftime(
            datetime.strptime(reg['updated_at'], '%Y-%m-%dT%H:%M:%S.%f'),
            '%d/%m/%Y %H:%M:%S')
        return f"""{reg['nota']}

        Fecha de Creación: {f_creacion}
        Fecha de Actualización: {f_actualizacion}"""

    def import_notas(self, username, user2link2):
        sql = f"""
            select n.id,
                n.nota, n.created_at, n.updated_at,
                ic.usuario as created_by, iu.usuario as updated_by
            from initsys_nota n
            inner join initsys_usr usr on usr.idusuario = n.usuario_id
            inner join initsys_usr ic on ic.idusuario = n.created_by_id
            inner join initsys_usr iu on iu.idusuario = n.updated_by_id
            where usr.usuario='{username}'
            order by n.created_at, n.updated_at;
            """.strip()
        regs = JsonRequest(self.url, {'getrows': 'yes', 'sql': sql})
        for row in regs:
            Nota.objects.get_or_create(
                user=user2link2,
                nota=self.create_nota(row),
                creado_por=self.responsables[row['created_by']],
                actualizado_por=self.responsables[row['updated_by']],
            )

    def import_alertas(self, username, user2link2):
        sql = f"""
            select a.id,
                a.nota, a.fecha_alerta, a.alertado, a.fecha_alertado,
                a.mostrar_alerta, a.fecha_no_mostrar,
                a.created_at, a.updated_at,
                ic.usuario as created_by, iu.usuario as updated_by
            from initsys_alerta a
            inner join initsys_usr usr on usr.idusuario = a.usuario_id
            inner join initsys_usr ic on ic.idusuario = a.created_by_id
            inner join initsys_usr iu on iu.idusuario = a.updated_by_id
            where usr.usuario='{username}'
            order by a.created_at, a.updated_at;
            """.strip()
        regs = JsonRequest(self.url, {'getrows': 'yes', 'sql': sql})
        for row in regs:
            Alerta.objects.get_or_create(
                user=user2link2,
                nota=self.create_nota(row),
                fecha_alerta=row['fecha_alerta'],
                alertado=row['alertado'],
                fecha_alertado=row['fecha_alertado'],
                mostrar_alerta=row['mostrar_alerta'],
                fecha_no_mostrar=row['fecha_no_mostrar'],
                creado_por=self.responsables[row['created_by']],
                actualizado_por=self.responsables[row['updated_by']],
            )
