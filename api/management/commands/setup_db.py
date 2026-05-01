import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection, transaction
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Sistema de Auto-Setup: Migra la BD y puebla datos iniciales si faltan'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== SISTEMA DE AUTO-SETUP CUADRA ERRE ==='))

        # 1. Asegurar Migraciones
        self.stdout.write('Verificando estructura de tablas...')
        try:
            call_command('migrate', interactive=False, verbosity=0)
            self.stdout.write(self.style.SUCCESS('Estructura de tablas OK.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error en migraciones: {e}'))
            return

        # 2. Poblar Datos Base
        try:
            self.seed_all()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al poblar datos: {e}'))

        self.stdout.write(self.style.SUCCESS('=== AUTO-SETUP FINALIZADO ===\n'))

    def seed_all(self):
        from api.models import (
            Rol, Usuario, CatalogoEspecialidad, CatalogoEstadoSesion, 
            CatalogoEstadoPago, CatalogoObjetivo, CatalogoDiagnostico,
            CatalogoEstadoCaballo, CatalogoParentesco, Terapeuta,
            CatalogoEventoEquino
        )

        # A. ROLES
        Rol.objects.get_or_create(nombre='Administrador')
        Rol.objects.get_or_create(nombre='Admin')
        tera_rol, _ = Rol.objects.get_or_create(nombre='Terapeuta')
        self.stdout.write('Roles verificados.')

        # B. USUARIO ADMIN
        admin_email = 'admin@cuadraerre.com'
        if not Usuario.objects.filter(email=admin_email).exists():
            admin_rol = Rol.objects.filter(nombre__in=['Administrador', 'Admin']).first()
            Usuario.objects.create(
                rol=admin_rol,
                email=admin_email,
                password=make_password('12345678'),
                nombre_completo='Admin Cuadra Erre',
                activo=True
            )
            self.stdout.write('Usuario Admin creado.')

        # C. CATÁLOGOS BASE (Usando filter().exists() para seguridad total)
        catalogos = {
            CatalogoEstadoSesion: ['Programada', 'En Curso', 'Finalizada', 'Cancelada'],
            CatalogoEstadoPago: ['Pendiente', 'Pagado', 'Vencido', 'Condonado'],
            CatalogoEstadoCaballo: ['Activo', 'Reposo', 'Atencion Medica', 'Retirado'],
            CatalogoParentesco: ['Madre', 'Padre', 'Abuelo/a', 'Tutor Legal', 'Hermano/a', 'Tio/a', 'Otro'],
            CatalogoEventoEquino: ['Vacuna', 'Herraje', 'Lesión', 'Atención Veterinaria', 'Desparasitación'],
            CatalogoObjetivo: [
                'Mejorar equilibrio', 'Control postural', 'Estimulacion sensorial',
                'Coordinacion motora', 'Relajacion y manejo de ansiedad', 'Socializacion',
                'Comunicacion verbal y no verbal', 'Fortalecimiento muscular',
                'Independencia funcional', 'Regulacion emocional'
            ],
            CatalogoDiagnostico: [
                'Paralisis Cerebral Infantil (PCI)', 'Trastorno del Espectro Autista (TEA)',
                'Sindrome de Down', 'TDAH', 'Discapacidad intelectual',
                'Trastorno del lenguaje', 'Retraso psicomotor', 'Distrofia muscular',
                'Lesion medular', 'Trastorno de ansiedad'
            ]
        }

        for model, items in catalogos.items():
            count = 0
            for nombre in items:
                if not model.objects.filter(nombre=nombre).exists():
                    model.objects.create(nombre=nombre)
                    count += 1
            if count > 0:
                self.stdout.write(f'Catálogo {model.__name__}: {count} nuevos registros.')

        # D. ESPECIALIDADES Y STAFF
        staff_data = [
            {"nombre": "Emmanuel Urbina", "email": "emmanuel.urbina@cuadraerre.com", "especialidad": "Fundador y Ranchero", "biografia": "NUESTRO FUNDADOR Y EL CORAZON QUE HACE LATIR A NUESTRA CUADRA."},
            {"nombre": "Jose Tejeda Noriega", "email": "jose.tejeda@cuadraerre.com", "especialidad": "Arrendador y Experto Charro", "biografia": "Arrendador y experto charro con +30 años de experiencia."},
            {"nombre": "Valentina Gonzalez", "email": "valentina.gonzalez@cuadraerre.com", "especialidad": "Administración y Equinoterapia", "biografia": "Licenciada en ADMINISTRAcion por la uam."},
            {"nombre": "María Luisa Gutiérrez", "email": "marialuisa.gutierrez@cuadraerre.com", "especialidad": "Dirección CRED", "biografia": "Directora del CRED-Sede Cuadra Erre."},
            {"nombre": "Valeria Camacho", "email": "valeria.camacho@cuadraerre.com", "especialidad": "Psicopedagogía", "biografia": "LICENCIADA EN PSICOLOGIA Y EQUINOTERAPEUTA."},
            {"nombre": "Sara Valencia", "email": "sara.valencia@cuadraerre.com", "especialidad": "Fisioterapia", "biografia": "LICENCIADA EN FISIOTERAPIA Y EQUINOTERAPEUTA."},
            {"nombre": "Omar Santamarina", "email": "omar.santamarina@cuadraerre.com", "especialidad": "Área Clínica", "biografia": "Licenciado en fisioterapia con maestria en salud."},
            {"nombre": "Adriana Ramirez", "email": "adriana.ramirez@cuadraerre.com", "especialidad": "Alta Escuela y Fundadora Domecq", "biografia": "Fundadora del centro de rehabilitación ecuestre domecq."},
            {"nombre": "Samuel Aguirre", "email": "samuel.aguirre@cuadraerre.com", "especialidad": "Psicopedagogía Nacional", "biografia": "LICENCIADO EN PSICOPEDAGOGIA CON MAESTRIA."}
        ]

        for member in staff_data:
            esp_obj = CatalogoEspecialidad.objects.filter(nombre=member["especialidad"]).first()
            if not esp_obj:
                esp_obj = CatalogoEspecialidad.objects.create(nombre=member["especialidad"])
            
            user = Usuario.objects.filter(email=member["email"]).first()
            if not user:
                user = Usuario.objects.create(
                    rol=tera_rol,
                    email=member["email"],
                    password=make_password("cuadra123"),
                    nombre_completo=member["nombre"],
                    activo=True
                )
            
            if not Terapeuta.objects.filter(usuario=user).exists():
                Terapeuta.objects.create(
                    usuario=user,
                    especialidad=esp_obj,
                    biografia=member["biografia"]
                )
        self.stdout.write('Personal de Staff verificado.')
