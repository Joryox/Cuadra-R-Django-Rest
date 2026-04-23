from rest_framework import serializers
from api.models import (
    Role, Usuario, CaballoEstadoSalud, Caballo, Tutor, Paciente,
    Diagnosticos, PacientesDiagnosticos, ContactosEmergencia, Parentesco,
    BitacoraEquina, EstatusSesion, Terapeutas, Sesion, ReporteSesion,
    ReporteObjetivos, Objetivos, EstadosPago, Pagos
)
from django.contrib.auth.hashers import make_password


# ============== SERIALIZERS PARA CATÁLOGOS ==============

class RoleSerializer(serializers.ModelSerializer):
    """Serializer para Role."""
    class Meta:
        model = Role
        fields = ['id', 'nombre', 'descripcion', 'creacion', 'actualizacion']
        read_only_fields = ['id', 'creacion', 'actualizacion']


class CaballoEstadoSaludSerializer(serializers.ModelSerializer):
    """Serializer para CaballoEstadoSalud."""
    class Meta:
        model = CaballoEstadoSalud
        fields = ['id', 'descripcion', 'creacion', 'actualizacion']
        read_only_fields = ['id', 'creacion', 'actualizacion']


class EstatusSesionSerializer(serializers.ModelSerializer):
    """Serializer para EstatusSesion."""
    class Meta:
        model = EstatusSesion
        fields = ['id', 'descripcion', 'creacion', 'actualizacion']
        read_only_fields = ['id', 'creacion', 'actualizacion']


class EstadosPagoSerializer(serializers.ModelSerializer):
    """Serializer para EstadosPago."""
    class Meta:
        model = EstadosPago
        fields = ['id', 'descripcion', 'creacion', 'actualizacion']
        read_only_fields = ['id', 'creacion', 'actualizacion']


class ParentescoSerializer(serializers.ModelSerializer):
    """Serializer para Parentesco."""
    class Meta:
        model = Parentesco
        fields = ['id', 'descripcion', 'creacion', 'actualizacion']
        read_only_fields = ['id', 'creacion', 'actualizacion']


class DiagnosticosSerializer(serializers.ModelSerializer):
    """Serializer para Diagnosticos."""
    class Meta:
        model = Diagnosticos
        fields = ['id', 'descripcion', 'creacion', 'actualizacion']
        read_only_fields = ['id', 'creacion', 'actualizacion']


class ObjetivosSerializer(serializers.ModelSerializer):
    """Serializer para Objetivos."""
    class Meta:
        model = Objetivos
        fields = ['id', 'descripcion', 'creacion', 'actualizacion']
        read_only_fields = ['id', 'creacion', 'actualizacion']


# ============== SERIALIZERS PARA USUARIOS ==============

class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para Usuario con relación a Roles."""
    roles = RoleSerializer(many=True, read_only=True)
    rol_ids = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        many=True,
        write_only=True,
        source='roles'
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'usuario', 'nombres', 'apellidos', 'correo', 
            'roles', 'rol_ids', 'password', 'creacion', 'actualizacion'
        ]
        read_only_fields = ['id', 'creacion', 'actualizacion']

    def create(self, validated_data):
        """Crear usuario con password hasheado."""
        password = validated_data.pop('password')
        roles = validated_data.pop('roles', [])
        usuario = Usuario(**validated_data)
        usuario.password_hash = make_password(password)
        usuario.salt = ''
        usuario.save()
        if roles:
            usuario.roles.set(roles)
        return usuario

    def update(self, instance, validated_data):
        """Actualizar usuario."""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.password_hash = make_password(password)
        roles = validated_data.pop('roles', None)
        instance = super().update(instance, validated_data)
        if roles is not None:
            instance.roles.set(roles)
        return instance


class TutorSerializer(serializers.ModelSerializer):
    """Serializer para Tutor con Usuario anidado."""
    usuario = UsuarioSerializer(source='usuario_id', read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(),
        write_only=True
    )

    class Meta:
        model = Tutor
        fields = ['id', 'usuario', 'usuario_id', 'telefono', 'direccion', 'creacion', 'actualizacion']
        read_only_fields = ['id', 'creacion', 'actualizacion']


class TerapeutasSerializer(serializers.ModelSerializer):
    """Serializer para Terapeutas con Usuario anidado."""
    usuario = UsuarioSerializer(source='usuario_id', read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(),
        write_only=True
    )

    class Meta:
        model = Terapeutas
        fields = ['id', 'usuario', 'usuario_id', 'especialidad', 'creacion', 'actualizacion']
        read_only_fields = ['id', 'creacion', 'actualizacion']


# ============== SERIALIZERS PARA CABALLOS ==============

class CaballoSerializer(serializers.ModelSerializer):
    """Serializer para Caballo con estado de salud anidado."""
    estado_salud = CaballoEstadoSaludSerializer(read_only=True)
    estado_salud_id = serializers.PrimaryKeyRelatedField(
        queryset=CaballoEstadoSalud.objects.all(),
        write_only=True,
        source='estado_salud'
    )

    class Meta:
        model = Caballo
        fields = [
            'id', 'nombre', 'raza', 'edad', 'peso_max', 
            'sesiones_semanales_max', 'estado_salud', 'estado_salud_id', 
            'activo', 'creacion', 'actualizacion'
        ]
        read_only_fields = ['id', 'creacion', 'actualizacion']

    def validate_edad(self, value):
        """Validar que la edad sea positiva."""
        if value < 0:
            raise serializers.ValidationError("La edad no puede ser negativa.")
        return value

    def validate_peso_max(self, value):
        """Validar que el peso máximo sea positivo."""
        if value <= 0:
            raise serializers.ValidationError("El peso máximo debe ser mayor a 0.")
        return value


# ============== SERIALIZERS PARA PACIENTES ==============

class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para Paciente con Tutor y Caballo favorito anidados."""
    tutor = TutorSerializer(source='tutor_id', read_only=True)
    tutor_id = serializers.PrimaryKeyRelatedField(
        queryset=Tutor.objects.all(),
        write_only=True
    )
    caballo_favorito = CaballoSerializer(source='caballo_favorito_id', read_only=True)
    caballo_favorito_id = serializers.PrimaryKeyRelatedField(
        queryset=Caballo.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )

    class Meta:
        model = Paciente
        fields = [
            'id', 'tutor', 'tutor_id', 'nombre', 'edad', 'peso',
            'caballo_favorito', 'caballo_favorito_id', 'activo', 'creacion', 'actualizacion'
        ]
        read_only_fields = ['id', 'creacion', 'actualizacion']

    def validate_edad(self, value):
        """Validar que la edad sea válida."""
        if value < 0 or value > 120:
            raise serializers.ValidationError("La edad debe estar entre 0 y 120.")
        return value

    def validate_peso(self, value):
        """Validar que el peso sea positivo."""
        if value <= 0:
            raise serializers.ValidationError("El peso debe ser mayor a 0.")
        return value


class ContactosEmergenciaSerializer(serializers.ModelSerializer):
    """Serializer para ContactosEmergencia."""
    paciente = PacienteSerializer(source='paciente_id', read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.all(),
        write_only=True
    )
    parentesco = ParentescoSerializer(source='parentesco_id', read_only=True)
    parentesco_id = serializers.PrimaryKeyRelatedField(
        queryset=Parentesco.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )

    class Meta:
        model = ContactosEmergencia
        fields = [
            'id', 'paciente', 'paciente_id', 'nombre', 'telefono',
            'parentesco', 'parentesco_id', 'creacion', 'actualizacion'
        ]
        read_only_fields = ['id', 'creacion', 'actualizacion']


class PacientesDiagnosticosSerializer(serializers.ModelSerializer):
    """Serializer para PacientesDiagnosticos."""
    paciente = PacienteSerializer(source='paciente_id', read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.all(),
        write_only=True
    )
    diagnostico = DiagnosticosSerializer(read_only=True)
    diagnostico_id = serializers.PrimaryKeyRelatedField(
        queryset=Diagnosticos.objects.all(),
        write_only=True,
        source='diagnostico'
    )

    class Meta:
        model = PacientesDiagnosticos
        fields = [
            'id', 'paciente', 'paciente_id', 'diagnostico', 
            'diagnostico_id', 'creacion', 'actualizacion'
        ]
        read_only_fields = ['id', 'creacion', 'actualizacion']


# ============== SERIALIZERS PARA SESIONES ==============

class SesionSerializer(serializers.ModelSerializer):
    """Serializer para Sesion con relaciones anidadas."""
    terapeuta = TerapeutasSerializer(source='terapeuta_id', read_only=True)
    terapeuta_id = serializers.PrimaryKeyRelatedField(
        queryset=Terapeutas.objects.all(),
        write_only=True
    )
    paciente = PacienteSerializer(source='paciente_id', read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.all(),
        write_only=True
    )
    caballo = CaballoSerializer(source='caballo_id', read_only=True)
    caballo_id = serializers.PrimaryKeyRelatedField(
        queryset=Caballo.objects.all(),
        write_only=True
    )
    estatus = EstatusSesionSerializer(source='estatus_id', read_only=True)
    estatus_id = serializers.PrimaryKeyRelatedField(
        queryset=EstatusSesion.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )

    class Meta:
        model = Sesion
        fields = [
            'id', 'terapeuta', 'terapeuta_id', 'paciente', 'paciente_id',
            'caballo', 'caballo_id', 'fecha_hora', 'duracion', 
            'estatus', 'estatus_id', 'observaciones', 'creacion', 'actualizacion'
        ]
        read_only_fields = ['id', 'creacion', 'actualizacion']

    def validate_duracion(self, value):
        """Validar que la duración sea positiva."""
        if value <= 0:
            raise serializers.ValidationError("La duración debe ser mayor a 0 minutos.")
        return value


class ReporteSesionSerializer(serializers.ModelSerializer):
    """Serializer para ReporteSesion."""
    sesion = SesionSerializer(source='sesion_id', read_only=True)
    sesion_id = serializers.PrimaryKeyRelatedField(
        queryset=Sesion.objects.all(),
        write_only=True
    )

    class Meta:
        model = ReporteSesion
        fields = [
            'id', 'sesion', 'sesion_id', 'ansiedad_inicial', 'ansiedad_final',
            'notas_clinicas', 'creacion', 'actualizacion'
        ]
        read_only_fields = ['id', 'creacion', 'actualizacion']

    def validate(self, data):
        """Validar que los niveles de ansiedad sean válidos (0-10)."""
        ansiedad_inicial = data.get('ansiedad_inicial')
        ansiedad_final = data.get('ansiedad_final')
        
        if ansiedad_inicial is not None and (ansiedad_inicial < 0 or ansiedad_inicial > 10):
            raise serializers.ValidationError("Ansiedad inicial debe estar entre 0 y 10.")
        if ansiedad_final is not None and (ansiedad_final < 0 or ansiedad_final > 10):
            raise serializers.ValidationError("Ansiedad final debe estar entre 0 y 10.")
        
        return data


class ReporteObjetivosSerializer(serializers.ModelSerializer):
    """Serializer para ReporteObjetivos."""
    reporte_sesion = ReporteSesionSerializer(source='reporte_sesion_id', read_only=True)
    reporte_sesion_id = serializers.PrimaryKeyRelatedField(
        queryset=ReporteSesion.objects.all(),
        write_only=True
    )
    objetivo = ObjetivosSerializer(source='objetivo_id', read_only=True)
    objetivo_id = serializers.PrimaryKeyRelatedField(
        queryset=Objetivos.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )

    class Meta:
        model = ReporteObjetivos
        fields = [
            'id', 'reporte_sesion', 'reporte_sesion_id', 
            'objetivo', 'objetivo_id', 'creacion', 'actualizacion'
        ]
        read_only_fields = ['id', 'creacion', 'actualizacion']


# ============== SERIALIZERS PARA BITÁCORAS Y PAGOS ==============

class BitacoraEquinaSerializer(serializers.ModelSerializer):
    """Serializer para BitacoraEquina."""
    paciente = PacienteSerializer(source='paciente_id', read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.all(),
        write_only=True
    )
    caballo = CaballoSerializer(source='caballo_id', read_only=True)
    caballo_id = serializers.PrimaryKeyRelatedField(
        queryset=Caballo.objects.all(),
        write_only=True
    )

    class Meta:
        model = BitacoraEquina
        fields = [
            'id', 'paciente', 'paciente_id', 'caballo', 'caballo_id',
            'fecha_sesion', 'duracion_sesion', 'observaciones', 'creacion', 'actualizacion'
        ]
        read_only_fields = ['id', 'creacion', 'actualizacion']

    def validate_duracion_sesion(self, value):
        """Validar que la duración sea positiva."""
        if value <= 0:
            raise serializers.ValidationError("La duración debe ser mayor a 0 minutos.")
        return value


class PagosSerializer(serializers.ModelSerializer):
    """Serializer para Pagos."""
    tutor = TutorSerializer(source='tutor_id', read_only=True)
    tutor_id = serializers.PrimaryKeyRelatedField(
        queryset=Tutor.objects.all(),
        write_only=True
    )
    sesion = SesionSerializer(source='sesion_id', read_only=True)
    sesion_id = serializers.PrimaryKeyRelatedField(
        queryset=Sesion.objects.all(),
        write_only=True
    )
    estatus = EstadosPagoSerializer(source='estatus_id', read_only=True)
    estatus_id = serializers.PrimaryKeyRelatedField(
        queryset=EstadosPago.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )

    class Meta:
        model = Pagos
        fields = [
            'id', 'tutor', 'tutor_id', 'sesion', 'sesion_id',
            'monto', 'estatus', 'estatus_id', 'creacion', 'actualizacion'
        ]
        read_only_fields = ['id', 'creacion', 'actualizacion']

    def validate_monto(self, value):
        """Validar que el monto sea positivo."""
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a 0.")
        return value
