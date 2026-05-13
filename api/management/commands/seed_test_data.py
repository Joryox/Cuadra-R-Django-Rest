"""
Management command: seed_test_data
Crea un escenario de prueba completo para Cuadra Erre:
  - 3 terapeutas con paciente propio
  - 4 caballos (3 activos, 1 en reposo)
  - 3 tutores (uno por paciente menor de edad)
  - Sesiones en todos los estados: Programada, En Curso, Finalizada, Cancelada
  - Reportes con notas y recomendaciones para casa
  - Contactos de emergencia por paciente
  - Bitácoras equinas
  - Objetivos por sesión

Uso:
  python manage.py seed_test_data          # Crea todo
  python manage.py seed_test_data --reset  # Borra datos de prueba y recrea
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta, date
import random


class Command(BaseCommand):
    help = "Crea datos de prueba completos para Cuadra Erre"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Elimina los datos de prueba anteriores antes de recrearlos",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("\n=== SEED DE DATOS DE PRUEBA ==="))
        try:
            self._seed(reset=options["reset"])
            self._print_credentials()
            self.stdout.write(self.style.SUCCESS("\n=== SEED FINALIZADO ✓ ===\n"))
        except Exception as e:
            import traceback
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            traceback.print_exc()

    # ─────────────────────────────────────────────────────────────────────
    def _seed(self, reset=False):
        from api.models import (
            Rol, Usuario, CatalogoEspecialidad, CatalogoEstadoSesion,
            CatalogoEstadoCaballo, CatalogoParentesco, CatalogoDiagnostico,
            CatalogoObjetivo, CatalogoEventoEquino,
            Terapeuta, Caballo, BitacoraEquina,
            Paciente, PacienteDiagnostico, ContactoEmergencia,
            Sesion, ReporteSesion, ReporteObjetivo,
        )

        if reset:
            self.stdout.write("  Limpiando datos de prueba anteriores...")
            # Solo borra emails de prueba para no afectar datos reales
            TEST_EMAILS = [
                "test.terapeuta1@cuadraerre.com",
                "test.terapeuta2@cuadraerre.com",
                "test.terapeuta3@cuadraerre.com",
                "test.tutor1@cuadraerre.com",
                "test.tutor2@cuadraerre.com",
                "test.tutor3@cuadraerre.com",
            ]
            Usuario.objects.filter(email__in=TEST_EMAILS).delete()
            Paciente.objects.filter(nombre__startswith="[TEST]").delete()
            Caballo.objects.filter(nombre__startswith="[TEST]").delete()
            self.stdout.write("  Limpieza completada.")

        # ── CATÁLOGOS ──────────────────────────────────────────────────
        est_programada = CatalogoEstadoSesion.objects.get(nombre="Programada")
        est_en_curso   = CatalogoEstadoSesion.objects.get(nombre="En Curso")
        est_finalizada = CatalogoEstadoSesion.objects.get(nombre="Finalizada")
        est_cancelada  = CatalogoEstadoSesion.objects.get(nombre="Cancelada")

        est_activo     = CatalogoEstadoCaballo.objects.get(nombre="Activo")
        est_reposo     = CatalogoEstadoCaballo.objects.get(nombre="Reposo")

        parentesco_madre = CatalogoParentesco.objects.filter(nombre="Madre").first()
        parentesco_padre = CatalogoParentesco.objects.filter(nombre="Padre").first()

        dx_tea    = CatalogoDiagnostico.objects.get(nombre="Trastorno del Espectro Autista (TEA)")
        dx_down   = CatalogoDiagnostico.objects.get(nombre="Sindrome de Down")
        dx_pci    = CatalogoDiagnostico.objects.get(nombre="Paralisis Cerebral Infantil (PCI)")
        dx_tdah   = CatalogoDiagnostico.objects.get(nombre="TDAH")

        obj_equilibrio  = CatalogoObjetivo.objects.get(nombre="Mejorar equilibrio")
        obj_postural    = CatalogoObjetivo.objects.get(nombre="Control postural")
        obj_motor       = CatalogoObjetivo.objects.get(nombre="Coordinacion motora")
        obj_social      = CatalogoObjetivo.objects.get(nombre="Socializacion")
        obj_emocional   = CatalogoObjetivo.objects.get(nombre="Regulacion emocional")

        rol_terapeuta = Rol.objects.get(nombre="Terapeuta")
        rol_tutor,  _ = Rol.objects.get_or_create(nombre="Tutor")
        rol_paciente, _ = Rol.objects.get_or_create(nombre="Paciente")

        esp_psico,  _ = CatalogoEspecialidad.objects.get_or_create(nombre="Psicopedagogía")
        esp_fisio,  _ = CatalogoEspecialidad.objects.get_or_create(nombre="Fisioterapia")
        esp_clinica,_ = CatalogoEspecialidad.objects.get_or_create(nombre="Área Clínica")

        ev_vacuna,  _ = CatalogoEventoEquino.objects.get_or_create(nombre="Vacuna")
        ev_herraje, _ = CatalogoEventoEquino.objects.get_or_create(nombre="Herraje")
        ev_lesion,  _ = CatalogoEventoEquino.objects.get_or_create(nombre="Lesión")

        # ── TERAPEUTAS ────────────────────────────────────────────────
        self.stdout.write("  Creando terapeutas de prueba...")

        def get_or_create_terapeuta(email, nombre, especialidad_nombre, bio):
            user, _ = Usuario.objects.get_or_create(
                email=email,
                defaults={
                    "rol": rol_terapeuta,
                    "password": make_password("test1234"),
                    "nombre_completo": nombre,
                    "activo": True,
                },
            )
            tera, _ = Terapeuta.objects.get_or_create(
                usuario=user,
                defaults={"especialidad_text": especialidad_nombre, "biografia": bio},
            )
            return user, tera

        u_t1, t1 = get_or_create_terapeuta(
            "test.terapeuta1@cuadraerre.com",
            "Valeria Herrera",
            "Psicopedagogia Testing",
            "Terapeuta de prueba — Psicopedagogía. Cuenta de testing.",
        )
        u_t2, t2 = get_or_create_terapeuta(
            "test.terapeuta2@cuadraerre.com",
            "Carlos Mendoza",
            "Fisioterapia Testing",
            "Terapeuta de prueba — Fisioterapia. Cuenta de testing.",
        )
        u_t3, t3 = get_or_create_terapeuta(
            "test.terapeuta3@cuadraerre.com",
            "Ana Flores",
            "Area Clinica Testing",
            "Terapeuta de prueba — Área Clínica. Cuenta de testing.",
        )

        # ── TUTORES ───────────────────────────────────────────────────
        self.stdout.write("  Creando tutores de prueba...")

        def get_or_create_tutor(email, nombre):
            u, _ = Usuario.objects.get_or_create(
                email=email,
                defaults={
                    "rol": rol_tutor,
                    "password": make_password("tutor1234"),
                    "nombre_completo": nombre,
                    "activo": True,
                },
            )
            return u

        tutor1 = get_or_create_tutor("test.tutor1@cuadraerre.com", "Lucía Ramírez")
        tutor2 = get_or_create_tutor("test.tutor2@cuadraerre.com", "Roberto Sánchez")
        tutor3 = get_or_create_tutor("test.tutor3@cuadraerre.com", "Patricia Vega")

        # ── CABALLOS ──────────────────────────────────────────────────
        self.stdout.write("  Creando caballos de prueba...")

        def get_or_create_caballo(nombre, estado, max_kg, max_ses, raza):
            c, _ = Caballo.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "estado_salud": estado,
                    "peso_max_soporta": max_kg,
                    "sesiones_semanales_max": max_ses,
                    "raza": raza,
                },
            )
            return c

        caballo1 = get_or_create_caballo("[TEST] Luna",    est_activo, 80, 10, "Cuarto de Milla")
        caballo2 = get_or_create_caballo("[TEST] Tornado", est_activo, 90, 8,  "Azteca")
        caballo3 = get_or_create_caballo("[TEST] Canela",  est_activo, 70, 10, "Pura Sangre")
        caballo4 = get_or_create_caballo("[TEST] Rayo",    est_reposo, 85, 10, "Andaluz")

        # Bitácora para caballo en reposo
        if not BitacoraEquina.objects.filter(caballo=caballo4).exists():
            BitacoraEquina.objects.create(
                caballo=caballo4,
                tipo_evento=ev_lesion,
                descripcion_veterinaria="Lesión leve en pata delantera derecha. Reposo indicado por 2 semanas.",
                fecha_evento=date.today() - timedelta(days=3),
            )
        # Bitácora de vacuna para Luna
        if not BitacoraEquina.objects.filter(caballo=caballo1, tipo_evento=ev_vacuna).exists():
            BitacoraEquina.objects.create(
                caballo=caballo1,
                tipo_evento=ev_vacuna,
                descripcion_veterinaria="Vacuna anual aplicada sin complicaciones. Listo para sesiones.",
                fecha_registro=date.today() - timedelta(days=10),
                fecha_evento=date.today() - timedelta(days=10),
            )

        # ── PACIENTES ─────────────────────────────────────────────────
        self.stdout.write("  Creando pacientes de prueba...")

        def make_paciente(nombre, edad, peso, tutor, diagnostico, terapeuta_asignado, mayor=False):
            p, created = Paciente.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "fecha_nacimiento": date.today() - timedelta(days=365 * edad),
                    "peso_kg": peso,
                    "tutor": tutor,
                    "motivo_consulta": f"Paciente de prueba — {diagnostico.nombre}",
                    "activo": True,
                    "es_mayor_de_edad": mayor,
                },
            )
            # Diagnóstico
            PacienteDiagnostico.objects.get_or_create(
                paciente=p,
                diagnostico=diagnostico,
                defaults={"observaciones": "Diagnóstico de prueba."},
            )
            # Contacto emergencia
            if not ContactoEmergencia.objects.filter(paciente=p).exists():
                ContactoEmergencia.objects.create(
                    paciente=p,
                    nombre_completo=f"Contacto de {nombre.split()[1]}",
                    telefono=f"555{random.randint(1000000, 9999999)}",
                    parentesco=parentesco_madre if not mayor else parentesco_padre,
                )
            return p

        paciente1 = make_paciente("[TEST] Sofia Ramírez",  8,  32, tutor1, dx_tea,  t1)
        paciente2 = make_paciente("[TEST] Diego Sánchez",  12, 45, tutor2, dx_down, t2)
        paciente3 = make_paciente("[TEST] Isabella Vega",  6,  24, tutor3, dx_pci,  t3)
        # Paciente adulto (tutor3 actúa como contacto de emergencia)
        paciente4 = make_paciente("[TEST] Marco Torres", 20, 68, tutor3, dx_tdah, t1, mayor=True)

        # ── SESIONES EN TODOS LOS ESTADOS ────────────────────────────
        self.stdout.write("  Creando sesiones de prueba...")
        ahora = timezone.now()

        sesiones_spec = [
            # (terapeuta, paciente, caballo, delta_horas, estatus, duracion)
            # Terapeuta 1
            (t1, paciente1, caballo1, -48, est_finalizada, 60),
            (t1, paciente1, caballo1, -24, est_finalizada, 45),
            (t1, paciente4, caballo2, -2,  est_finalizada, 60),
            (t1, paciente1, caballo1, 2,   est_programada, 60),
            (t1, paciente4, caballo2, 26,  est_programada, 45),
            # Terapeuta 2
            (t2, paciente2, caballo2, -72, est_finalizada, 60),
            (t2, paciente2, caballo2, -48, est_finalizada, 60),
            (t2, paciente2, caballo3, -1,  est_en_curso,   60),
            (t2, paciente4, caballo3, 4,   est_programada, 45),
            # Terapeuta 3
            (t3, paciente3, caballo3, -96, est_finalizada, 60),
            (t3, paciente3, caballo1, -23, est_cancelada,  60),
            (t3, paciente3, caballo1, 3,   est_programada, 60),
            (t3, paciente3, caballo1, 27,  est_programada, 45),
        ]

        sesiones_creadas = []
        for (tera, pac, cab, delta_h, est, dur) in sesiones_spec:
            fh = ahora + timedelta(hours=delta_h)
            # Evitar duplicado exacto
            exists = Sesion.objects.filter(
                terapeuta=tera, paciente=pac, fecha_hora__date=fh.date(),
                estatus=est,
            ).exists()
            if not exists:
                s = Sesion.objects.create(
                    terapeuta=tera,
                    paciente=pac,
                    caballo=cab,
                    estatus=est,
                    fecha_hora=fh,
                    duracion_minutos=dur,
                )
                sesiones_creadas.append(s)
            else:
                # Recuperar existente para agregar reportes
                s = Sesion.objects.filter(
                    terapeuta=tera, paciente=pac, fecha_hora__date=fh.date(),
                    estatus=est,
                ).first()
                sesiones_creadas.append(s)

        # ── REPORTES DE SESIÓN ────────────────────────────────────────
        self.stdout.write("  Creando reportes clínicos...")

        notas_pool = [
            "Paciente mostró excelente disposición. Completó todos los ejercicios de equilibrio.",
            "Sesión con avance notable en coordinación postural. Permaneció montado 40 minutos.",
            "Se trabajó con el paciente en ejercicios de relajación sobre el caballo. Muy buena respuesta.",
            "El paciente logró mantener postura erguida por primera vez sin apoyo lateral.",
            "Sesión de menor duración por fatiga del paciente. Se concluyó con ejercicio respiratorio.",
            "Excelente sesión. El paciente verbalizó emociones durante la actividad por primera vez.",
        ]
        recomendaciones_pool = [
            "Practicar en casa: 10 min de ejercicios de equilibrio en tabla de madera o cojín.",
            "Realizar estiramientos de espalda baja por las mañanas durante 5 minutos.",
            "Continuar con rutina de respiración diafragmática antes de dormir.",
            "Fomentar actividades que requieran coordinación bilateral (lanzar pelota, bicicleta).",
            "Evitar pantallas 1 hora antes de dormir. Implementar rutina de relajación nocturna.",
            "Reforzar el vínculo emocional con el animal en casa con mascotas si es posible.",
        ]

        objetivos_pool = [obj_equilibrio, obj_postural, obj_motor, obj_social, obj_emocional]

        for s in sesiones_creadas:
            if s and s.estatus == est_finalizada:
                if not ReporteSesion.objects.filter(sesion=s).exists():
                    reporte = ReporteSesion.objects.create(
                        sesion=s,
                        notas_clinicas=random.choice(notas_pool),
                        recomendacion_casa=random.choice(recomendaciones_pool),
                        ansiedad_inicial=random.randint(4, 8),
                        ansiedad_final=random.randint(1, 4),
                    )
                    # Agregar 2 objetivos al reporte
                    for obj in random.sample(objetivos_pool, k=2):
                        ReporteObjetivo.objects.get_or_create(
                            reporte=reporte, objetivo=obj,
                        )

    # ─────────────────────────────────────────────────────────────────────
    def _print_credentials(self):
        creds = [
            ("ADMINISTRADOR",  "admin@cuadraerre.com",             "12345678"),
            ("TERAPEUTA 1",    "test.terapeuta1@cuadraerre.com",   "test1234"),
            ("TERAPEUTA 2",    "test.terapeuta2@cuadraerre.com",   "test1234"),
            ("TERAPEUTA 3",    "test.terapeuta3@cuadraerre.com",   "test1234"),
            ("TUTOR 1",        "test.tutor1@cuadraerre.com",       "tutor1234"),
            ("TUTOR 2",        "test.tutor2@cuadraerre.com",       "tutor1234"),
            ("TUTOR 3",        "test.tutor3@cuadraerre.com",       "tutor1234"),
        ]
        self.stdout.write(self.style.SUCCESS("\n╔══════════════════════════════════════════════════════╗"))
        self.stdout.write(self.style.SUCCESS("║         CREDENCIALES DE PRUEBA — CUADRA ERRE         ║"))
        self.stdout.write(self.style.SUCCESS("╠══════════════════════════════════════════════════════╣"))
        for rol, email, pw in creds:
            self.stdout.write(f"  {rol:<16}  {email:<42}  pw: {pw}")
        self.stdout.write(self.style.SUCCESS("╚══════════════════════════════════════════════════════╝"))
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("Datos de prueba:"))
        self.stdout.write("  Caballos:  [TEST] Luna · Tornado · Canela (activos) | Rayo (reposo)")
        self.stdout.write("  Pacientes: [TEST] Sofia (T1), Diego (T2), Isabella (T3), Marco (adulto-T1)")
        self.stdout.write("  Sesiones:  Finalizadas, En Curso, Programadas y Canceladas creadas")
        self.stdout.write("  Reportes:  Notas y recomendaciones para sesiones finalizadas")
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("Para resetear y recrear:"))
        self.stdout.write("  python manage.py seed_test_data --reset")
