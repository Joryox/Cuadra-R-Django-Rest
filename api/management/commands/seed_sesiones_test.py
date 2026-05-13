import random
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from api.models import Sesion, Paciente, Terapeuta, Caballo, CatalogoEstadoSesion

class Command(BaseCommand):
    help = 'Genera 3 sesiones de prueba en diferentes meses para probar el calendario'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando generación de sesiones de prueba...")

        pacientes = list(Paciente.objects.all())
        terapeutas = list(Terapeuta.objects.all())
        caballos = list(Caballo.objects.all())
        estado_programada = CatalogoEstadoSesion.objects.filter(nombre="Programada").first()

        if not (pacientes and terapeutas and caballos and estado_programada):
            self.stdout.write(self.style.ERROR("Faltan datos base (Pacientes, Terapeutas, Caballos o Estado Programada). Asegúrate de correr los seeders básicos primero."))
            return

        now = timezone.now()
        
        # Sesión 1: Mes Actual
        sesion1_fecha = now.replace(day=15, hour=10, minute=0, second=0, microsecond=0)
        if sesion1_fecha < now:
            sesion1_fecha = sesion1_fecha + timedelta(days=20) # ensure future or just any date

        Sesion.objects.create(
            paciente=random.choice(pacientes),
            terapeuta=random.choice(terapeutas),
            caballo=caballos[0 % len(caballos)],
            fecha_hora=sesion1_fecha,
            duracion_minutos=60,
            estatus=estado_programada
        )
        self.stdout.write(self.style.SUCCESS(f"Sesión 1 creada: {sesion1_fecha.strftime('%d/%m/%Y %H:%M')}"))

        # Sesión 2: Mes Próximo
        mes_proximo = (now.month % 12) + 1
        año_proximo = now.year + (1 if now.month == 12 else 0)
        sesion2_fecha = now.replace(year=año_proximo, month=mes_proximo, day=10, hour=12, minute=30, second=0, microsecond=0)
        
        Sesion.objects.create(
            paciente=random.choice(pacientes),
            terapeuta=random.choice(terapeutas),
            caballo=caballos[1 % len(caballos)],
            fecha_hora=sesion2_fecha,
            duracion_minutos=60,
            estatus=estado_programada
        )
        self.stdout.write(self.style.SUCCESS(f"Sesión 2 creada: {sesion2_fecha.strftime('%d/%m/%Y %H:%M')}"))

        # Sesión 3: En dos meses
        mes_dos = ((now.month + 1) % 12) + 1
        año_dos = now.year + (1 if now.month >= 11 else 0)
        sesion3_fecha = now.replace(year=año_dos, month=mes_dos, day=5, hour=16, minute=0, second=0, microsecond=0)

        Sesion.objects.create(
            paciente=random.choice(pacientes),
            terapeuta=random.choice(terapeutas),
            caballo=caballos[2 % len(caballos)],
            fecha_hora=sesion3_fecha,
            duracion_minutos=60,
            estatus=estado_programada
        )
        self.stdout.write(self.style.SUCCESS(f"Sesión 3 creada: {sesion3_fecha.strftime('%d/%m/%Y %H:%M')}"))

        self.stdout.write(self.style.SUCCESS("¡Generación completada exitosamente!"))
