import uuid
from django.db import models

# ==========================================
# MÓDULO 1: SEGURIDAD (RBAC)
# ==========================================
class Rol(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Admin, Terapeuta, Tutor

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) # Hash
    nombre_completo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_completo

# ==========================================
# MÓDULO 2: CATÁLOGOS MAESTROS
# ==========================================
class CatalogoEspecialidad(models.Model):
    nombre = models.CharField(max_length=100) # Ej: Fisioterapia, Psicología
    def __str__(self): return self.nombre

class CatalogoDiagnostico(models.Model):
    nombre = models.CharField(max_length=100) # Ej: PCI, TEA, Síndrome de Down
    def __str__(self): return self.nombre

class CatalogoObjetivo(models.Model):
    nombre = models.CharField(max_length=255) # Ej: Mejorar equilibrio
    def __str__(self): return self.nombre

class CatalogoEstadoCaballo(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Activo, Reposo, Atención Médica
    def __str__(self): return self.nombre

class CatalogoEventoEquino(models.Model):
    nombre = models.CharField(max_length=100) # Ej: Vacuna, Herraje, Lesión
    def __str__(self): return self.nombre

class CatalogoEstadoSesion(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Programada, En Curso, Finalizada, Cancelada
    def __str__(self): return self.nombre

class CatalogoEstadoPago(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Pendiente, Pagado, Vencido, Condonado
    def __str__(self): return self.nombre

class CatalogoParentesco(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Madre, Padre, Abuelo/a, Tutor Legal
    def __str__(self): return self.nombre

# ==========================================
# MÓDULO 3: EQUIPO CLÍNICO
# ==========================================
class Terapeuta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    especialidad = models.ForeignKey(CatalogoEspecialidad, on_delete=models.PROTECT)
    cedula_profesional = models.CharField(max_length=50, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    disponible = models.BooleanField(default=True)  # Switch: vacaciones/fuera de servicio
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.especialidad.nombre}"

# ==========================================
# MÓDULO 5: ACTIVOS Y BIENESTAR ANIMAL
# ==========================================
class Caballo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado_salud = models.ForeignKey(CatalogoEstadoCaballo, on_delete=models.PROTECT)
    peso_max_soporta = models.DecimalField(max_digits=5, decimal_places=2) # En kg
    sesiones_semanales_max = models.IntegerField()
    raza = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)  # Archivado (borrado lógico)
    disponible = models.BooleanField(default=True)  # Switch: descanso
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)
    motivo_inactividad = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class BitacoraEquina(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    caballo = models.ForeignKey(Caballo, on_delete=models.PROTECT)
    fecha_registro = models.DateField(auto_now_add=True)
    tipo_evento = models.ForeignKey(CatalogoEventoEquino, on_delete=models.PROTECT)
    descripcion_veterinaria = models.TextField()

# ==========================================
# MÓDULO 4: PACIENTES Y FAMILIAS
# ==========================================
class Paciente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tutor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='pacientes_tutorados')
    caballo_favorito = models.ForeignKey(Caballo, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)
    
    # Historial Clínico
    es_mayor_de_edad = models.BooleanField(default=False)
    estado_civil = models.CharField(max_length=50, blank=True, null=True)
    ocupacion_escolaridad = models.CharField(max_length=200, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    contacto_emergencia = models.CharField(max_length=255, blank=True, null=True)
    tutor_secundario_nombre = models.CharField(max_length=255, blank=True, null=True)
    tutor_secundario_telefono = models.CharField(max_length=20, blank=True, null=True)
    motivo_consulta = models.TextField(blank=True, null=True)
    historial_medico = models.TextField(blank=True, null=True)
    antecedentes_familiares = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class PacienteDiagnostico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    diagnostico = models.ForeignKey(CatalogoDiagnostico, on_delete=models.PROTECT)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('paciente', 'diagnostico')

class ContactoEmergencia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    parentesco = models.ForeignKey(CatalogoParentesco, on_delete=models.PROTECT)
    nombre_completo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

# ==========================================
# MÓDULO 6: OPERACIÓN CLÍNICA (CORE)
# ==========================================
class Sesion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    terapeuta = models.ForeignKey(Terapeuta, on_delete=models.PROTECT)
    caballo = models.ForeignKey(Caballo, on_delete=models.PROTECT)
    fecha_hora = models.DateTimeField()
    estatus = models.ForeignKey(CatalogoEstadoSesion, on_delete=models.PROTECT)

    def __str__(self):
        return f"Sesion: {self.paciente.nombre} - {self.fecha_hora.strftime('%d/%m/%Y')}"

class ReporteSesion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sesion = models.OneToOneField(Sesion, on_delete=models.PROTECT)
    ansiedad_inicial = models.IntegerField(help_text="Escala del 1 al 10")
    ansiedad_final = models.IntegerField(help_text="Escala del 1 al 10")
    notas_clinicas = models.TextField()
    recomendacion_casa = models.TextField()

class ReporteObjetivo(models.Model):
    reporte = models.ForeignKey(ReporteSesion, on_delete=models.CASCADE)
    objetivo = models.ForeignKey(CatalogoObjetivo, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('reporte', 'objetivo')

# ==========================================
# MÓDULO 7: ADMINISTRACIÓN FINANCIERA
# ==========================================
class Pago(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tutor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='pagos_tutor')
    sesion = models.ForeignKey(Sesion, on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estatus = models.ForeignKey(CatalogoEstadoPago, on_delete=models.PROTECT)
    fecha_limite = models.DateField()
    fecha_pago = models.DateField(auto_now_add=True, null=True, blank=True)
    comprobante = models.FileField(upload_to='pagos/', blank=True, null=True)

    def __str__(self):
        return f"Pago: {self.tutor.nombre_completo} - ${self.monto}"

# ==========================================
# MÓDULO 8: SEGURIDAD Y AUDITORÍA
# ==========================================
class BitacoraSeguridad(models.Model):
    TIPOS_EVENTO = (
        ('LOGIN', 'Inicio de Sesión'),
        ('PASSWORD_CHANGE', 'Cambio de Contraseña'),
        ('ARCHIVE', 'Registro Archivado'),
        ('RESTORE', 'Registro Restaurado'),
        ('CRITICAL_CONFIG', 'Cambio en Configuración Crítica'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario_afectado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_recibidos')
    usuario_accion = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='eventos_realizados')
    tipo_evento = models.CharField(max_length=50, choices=TIPOS_EVENTO)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Bitácora de Seguridad"
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.tipo_evento} - {self.usuario_afectado.email} - {self.fecha_hora}"