from rest_framework import serializers
from api.models import (
    Rol, Usuario, CatalogoEspecialidad, CatalogoDiagnostico,
    CatalogoObjetivo, CatalogoEstadoCaballo, CatalogoEventoEquino,
    CatalogoEstadoSesion, CatalogoEstadoPago, CatalogoParentesco,
    Terapeuta, Caballo, BitacoraEquina, Paciente, PacienteDiagnostico,
    ContactoEmergencia, Sesion, ReporteSesion, ReporteObjetivo, Pago,
    BitacoraSeguridad
)

# --- Catálogos ---
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class CatalogoEspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEspecialidad
        fields = '__all__'

class CatalogoDiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoDiagnostico
        fields = '__all__'

class CatalogoObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoObjetivo
        fields = '__all__'

class CatalogoEstadoCaballoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEstadoCaballo
        fields = '__all__'

class CatalogoEventoEquinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEventoEquino
        fields = '__all__'

class CatalogoEstadoSesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEstadoSesion
        fields = '__all__'

class CatalogoEstadoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEstadoPago
        fields = '__all__'

class CatalogoParentescoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoParentesco
        fields = '__all__'

# --- Modelos Core ---
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class TerapeutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terapeuta
        fields = '__all__'
        depth = 1

class CaballoSerializer(serializers.ModelSerializer):
    ultimo_evento = serializers.SerializerMethodField()

    class Meta:
        model = Caballo
        fields = '__all__'
        depth = 1

    def get_ultimo_evento(self, obj):
        evento = obj.bitacoraequina_set.order_by('-fecha_evento', '-hora_evento', '-fecha_registro').first()
        if evento:
            return {
                "tipo": evento.tipo_evento.nombre,
                "descripcion": evento.descripcion_veterinaria,
                "fecha": evento.fecha_registro.strftime("%Y-%m-%d")
            }
        return None

class CaballoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caballo
        fields = '__all__'

class BitacoraEquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitacoraEquina
        fields = '__all__'
        depth = 1

class BitacoraEquinaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitacoraEquina
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    tutor_nombre = serializers.CharField(source='tutor.nombre_completo', read_only=True)
    
    class Meta:
        model = Paciente
        fields = '__all__'
        depth = 1

class PacienteDiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteDiagnostico
        fields = '__all__'

class ContactoEmergenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactoEmergencia
        fields = '__all__'

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = '__all__'
        depth = 2

class SesionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = '__all__'

class ReporteSesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteSesion
        fields = '__all__'
        depth = 1

class ReporteSesionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteSesion
        fields = '__all__'


class ReporteObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteObjetivo
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class BitacoraSeguridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitacoraSeguridad
        fields = '__all__'
        depth = 1

