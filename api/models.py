from django.db import models

class Role(models.Model):
    id = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    eliminado = models.BooleanField(default=False)
    creacion = models.DateTimeField(auto_now_add=True, null=True)
    actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'roles'
        
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=255, unique=True)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    correo = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)    
    roles = models.ManyToManyField(
        Role, 
        related_name="usuarios",
        db_table="usuarios_roles" 
    )
    
    creacion = models.DateTimeField(auto_now_add=True, null=True)
    actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'usuarios'

class CaballoEstadoSalud(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    creacion = models.DateTimeField(auto_now_add=True, null=True)
    actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'estados_salud'

class Caballo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    raza = models.CharField(max_length=255)
    edad = models.IntegerField()
    peso_max = models.FloatField()
    sesiones_semanales_max = models.IntegerField()
    estado_salud = models.ForeignKey(
        CaballoEstadoSalud, 
        on_delete=models.RESTRICT,
        related_name="history"
    )
    
    activo = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    creacion = models.DateTimeField(auto_now_add=True, null=True)
    actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'caballos'
        
class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_id = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE
    )
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    creacion = models.DateTimeField(auto_now_add=True, null=True)
    actualizacion = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'tutores'
        
class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    tutor_id = models.ForeignKey(
        Tutor, 
        on_delete=models.CASCADE
    )
    caballo_favorito_id = models.ForeignKey(
        Caballo, 
        on_delete=models.SET_NULL,
        null=True
    )
    nombre = models.CharField(max_length=255)
    edad = models.IntegerField()
    peso = models.FloatField()
    activo = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    creacion = models.DateTimeField(auto_now_add=True, null=True)
    actualizacion = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'pacientes'
        
class BitacoraEquina(models.Model):
    id = models.AutoField(primary_key=True)
    paciente_id = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE
    )
    caballo_id = models.ForeignKey(
        Caballo, 
        on_delete=models.CASCADE
    )
    fecha_sesion = models.DateTimeField()
    duracion_sesion = models.IntegerField()  # Duración en minutos
    observaciones = models.TextField(null=True, blank=True)
    creacion = models.DateTimeField(auto_now_add=True, null=True)
    actualizacion = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'bitacoras_equinas'