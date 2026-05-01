import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_config.settings')
django.setup()

from api.models import Usuario, Rol, Terapeuta, CatalogoEspecialidad, CatalogoEstadoCaballo, Caballo
from django.contrib.auth.hashers import make_password

def seed_staff():
    # 1. Asegurar Roles
    admin_rol, _ = Rol.objects.get_or_create(nombre='Admin')
    tera_rol, _ = Rol.objects.get_or_create(nombre='Terapeuta')

    # 2. Asegurar Especialidades
    especialidades_data = [
        "Fundador y Ranchero",
        "Arrendador y Experto Charro",
        "Administración y Equinoterapia",
        "Dirección CRED",
        "Psicopedagogía",
        "Fisioterapia",
        "Área Clínica",
        "Alta Escuela y Fundadora Domecq",
        "Psicopedagogía Nacional"
    ]
    
    especialidades_obj = {}
    for nombre in especialidades_data:
        obj, _ = CatalogoEspecialidad.objects.get_or_create(nombre=nombre)
        especialidades_obj[nombre] = obj

    # 3. Datos del Staff
    staff_data = [
        {
            "nombre": "Emmanuel Urbina",
            "email": "emmanuel.urbina@cuadraerre.com",
            "especialidad": "Fundador y Ranchero",
            "biografia": "NUESTRO FUNDADOR Y EL CORAZON QUE HACE LATIR A NUESTRA CUADRA. INGENIERO DE PROFESION PERO RANCHERO POR CONVICCION"
        },
        {
            "nombre": "Jose Tejeda Noriega",
            "email": "jose.tejeda@cuadraerre.com",
            "especialidad": "Arrendador y Experto Charro",
            "biografia": "Arrendador y experto charro con +30 años de experiencia Y GANADOR DE COMPETENCIAS DE RODEO INTERNACIONALES"
        },
        {
            "nombre": "Valentina Gonzalez",
            "email": "valentina.gonzalez@cuadraerre.com",
            "especialidad": "Administración y Equinoterapia",
            "biografia": "licenciada en ADMINISTRAcion por la uam, es nuestra administradora con certificación en equinoterapia"
        },
        {
            "nombre": "María Luisa Gutiérrez",
            "email": "marialuisa.gutierrez@cuadraerre.com",
            "especialidad": "Dirección CRED",
            "biografia": "directora del cred-sede cuadra erre y madre que trabaja para que todas las mamás cabeñas tengan un espacio para una rehabilitación digna y eficaz"
        },
        {
            "nombre": "Valeria Camacho",
            "email": "valeria.camacho@cuadraerre.com",
            "especialidad": "Psicopedagogía",
            "biografia": "LICENCIADA EN PSICOLOGIA Y EQUINOTERAPEUTA DE AMPLIA EXPERIENCIA A CARGO DEL AREA DE PSICOPEDAGOGIA EN CRED-CUADRA ERRE"
        },
        {
            "nombre": "Sara Valencia",
            "email": "sara.valencia@cuadraerre.com",
            "especialidad": "Fisioterapia",
            "biografia": "LICENCIADA EN FISIOTERAPIA Y EQUINOTERAPEUTA de excelencia A CARGO DEL AREA DE fisioterapia EN CRED-CUADRA ERRE"
        },
        {
            "nombre": "Omar Santamarina",
            "email": "omar.santamarina@cuadraerre.com",
            "especialidad": "Área Clínica",
            "biografia": "licenciado en fisioterapia con maestria en salud y diversas certificaciones nacioanles e internacionales en equinoterapia a cargo del area clinica de cred-cuadra erre y coordinador nacional de fisioterapia en centro de rehabilitación ecuestre domecq"
        },
        {
            "nombre": "Adriana Ramirez",
            "email": "adriana.ramirez@cuadraerre.com",
            "especialidad": "Alta Escuela y Fundadora Domecq",
            "biografia": "fundadora del centro de rehabilitación ecuestre domecq, primera mujer graduada de jinete de alta escuela en mexico y gran innovadora de la terapia con equinos en mexico que con generosidad y valor ha creado esta realidad de màs de 1000 terapias anuales entre todas las sedes que ha logrado generar"
        },
        {
            "nombre": "Samuel Aguirre",
            "email": "samuel.aguirre@cuadraerre.com",
            "especialidad": "Psicopedagogía Nacional",
            "biografia": "LICENCIADO EN PSICOPEDAGOGIA CON MAESTRIA EN EL AREA DE LA SALUD Y CERTIFICACION EN EQUINOTERAPIA A CARGO DEL AREA DE PSICOPEDAGOGIA A NIVEL NACIONAL EN CENTRO DE REHABILITACIÓN ECUESTRE DOMECQ"
        }
    ]

    for member in staff_data:
        # Crear/Actualizar Usuario
        user, created = Usuario.objects.get_or_create(
            email=member["email"],
            defaults={
                "nombre_completo": member["nombre"],
                "rol": tera_rol,
                "password": make_password("cuadra123"),
                "activo": True
            }
        )
        if not created:
            user.nombre_completo = member["nombre"]
            user.save()

        # Crear/Actualizar Terapeuta
        Terapeuta.objects.update_or_create(
            usuario=user,
            defaults={
                "especialidad": especialidades_obj[member["especialidad"]],
                "biografia": member["biografia"]
            }
        )
    
    print("Staff sembrado exitosamente.")

if __name__ == "__main__":
    seed_staff()
