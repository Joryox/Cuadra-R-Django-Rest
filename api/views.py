from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Count, Sum
from django.utils import timezone
import jwt, datetime, os
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from api.models import (
    Rol, Usuario, CatalogoEspecialidad, CatalogoDiagnostico,
    CatalogoObjetivo, CatalogoEstadoCaballo, CatalogoEventoEquino,
    CatalogoEstadoSesion, CatalogoEstadoPago, CatalogoParentesco,
    Terapeuta, Caballo, BitacoraEquina, Paciente, PacienteDiagnostico,
    ContactoEmergencia, Sesion, ReporteSesion, ReporteObjetivo, Pago,
    BitacoraSeguridad
)
from api.serializers import (
    RolSerializer, UsuarioSerializer, CatalogoEspecialidadSerializer,
    CatalogoDiagnosticoSerializer, CatalogoObjetivoSerializer,
    CatalogoEstadoCaballoSerializer, CatalogoEventoEquinoSerializer,
    CatalogoEstadoSesionSerializer, CatalogoEstadoPagoSerializer,
    CatalogoParentescoSerializer, TerapeutaSerializer, CaballoSerializer,
    CaballoWriteSerializer, BitacoraEquinaSerializer, BitacoraEquinaWriteSerializer,
    PacienteSerializer, PacienteDiagnosticoSerializer, ContactoEmergenciaSerializer,
    SesionSerializer, SesionWriteSerializer, ReporteSesionSerializer,
    ReporteSesionWriteSerializer, ReporteObjetivoSerializer, PagoSerializer,
    BitacoraSeguridadSerializer
)
import httpx

# --- Catálogos ---
@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [AllowAny]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoEspecialidadViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEspecialidad.objects.all()
    serializer_class = CatalogoEspecialidadSerializer
    permission_classes = [AllowAny]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoDiagnosticoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoDiagnostico.objects.all()
    serializer_class = CatalogoDiagnosticoSerializer
    permission_classes = [AllowAny]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoObjetivoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoObjetivo.objects.all()
    serializer_class = CatalogoObjetivoSerializer
    permission_classes = [AllowAny]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoEstadoCaballoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEstadoCaballo.objects.all()
    serializer_class = CatalogoEstadoCaballoSerializer
    permission_classes = [AllowAny]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoEventoEquinoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEventoEquino.objects.all()
    serializer_class = CatalogoEventoEquinoSerializer
    permission_classes = [AllowAny]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoEstadoSesionViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEstadoSesion.objects.all()
    serializer_class = CatalogoEstadoSesionSerializer
    permission_classes = [AllowAny]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoEstadoPagoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEstadoPago.objects.all()
    serializer_class = CatalogoEstadoPagoSerializer
    permission_classes = [AllowAny]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoParentescoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoParentesco.objects.all()
    serializer_class = CatalogoParentescoSerializer
    permission_classes = [AllowAny]
    pagination_class = None

# --- Modelos Core ---
@extend_schema_view(
    list=extend_schema(tags=['Usuarios']),
    retrieve=extend_schema(tags=['Usuarios']),
    create=extend_schema(tags=['Usuarios']),
    update=extend_schema(tags=['Usuarios']),
    partial_update=extend_schema(tags=['Usuarios']),
    destroy=extend_schema(tags=['Usuarios']),
)
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]

@extend_schema_view(
    list=extend_schema(tags=['Usuarios']),
    retrieve=extend_schema(tags=['Usuarios']),
    create=extend_schema(tags=['Usuarios']),
    update=extend_schema(tags=['Usuarios']),
    partial_update=extend_schema(tags=['Usuarios']),
    destroy=extend_schema(tags=['Usuarios']),
)
class TerapeutaViewSet(viewsets.ModelViewSet):
    queryset = Terapeuta.objects.all()
    serializer_class = TerapeutaSerializer
    permission_classes = [AllowAny]
    authentication_classes = [] # Desactivado temporalmente para restaurar visibilidad
    pagination_class = None

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        usuario = instance.usuario
        usuario.activo = False
        usuario.save()
        return Response({"message": "Terapeuta dado de baja (borrado logico)."}, status=status.HTTP_200_OK)

@extend_schema_view(
    list=extend_schema(tags=['Caballos']),
    retrieve=extend_schema(tags=['Caballos']),
    create=extend_schema(tags=['Caballos']),
    update=extend_schema(tags=['Caballos']),
    partial_update=extend_schema(tags=['Caballos']),
    destroy=extend_schema(tags=['Caballos']),
)
class CaballoViewSet(viewsets.ModelViewSet):
    queryset = Caballo.objects.all().order_by('-fecha_registro')
    serializer_class = CaballoSerializer
    authentication_classes = [] # Desactivado temporalmente
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CaballoWriteSerializer
        return CaballoSerializer

    def partial_update(self, request, *args, **kwargs):
        # Sincronización automática de estado_salud con disponible
        if 'disponible' in request.data:
            disponible = request.data.get('disponible')
            # ID 1: Activo, ID 2: Reposo
            request.data['estado_salud'] = 1 if disponible else 2
            
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.activo = False
        instance.save()
        return Response({"message": "Caballo dado de baja (borrado lógico)."}, status=status.HTTP_200_OK)

@extend_schema_view(
    list=extend_schema(tags=['Caballos']),
    retrieve=extend_schema(tags=['Caballos']),
    create=extend_schema(tags=['Caballos']),
    update=extend_schema(tags=['Caballos']),
    partial_update=extend_schema(tags=['Caballos']),
    destroy=extend_schema(tags=['Caballos']),
)
class BitacoraEquinaViewSet(viewsets.ModelViewSet):
    queryset = BitacoraEquina.objects.all().order_by('-fecha_evento', '-hora_evento', '-fecha_registro')
    serializer_class = BitacoraEquinaSerializer
    filterset_fields = ['caballo']
    permission_classes = [AllowAny]
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BitacoraEquinaWriteSerializer
        return BitacoraEquinaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        caballo_id = self.request.query_params.get('caballo')
        if caballo_id:
            qs = qs.filter(caballo_id=caballo_id)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(tags=['Pacientes']),
    retrieve=extend_schema(tags=['Pacientes']),
    create=extend_schema(tags=['Pacientes']),
    update=extend_schema(tags=['Pacientes']),
    partial_update=extend_schema(tags=['Pacientes']),
    destroy=extend_schema(tags=['Pacientes']),
)
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = None

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.activo = False
        instance.save()
        return Response({"message": "Paciente dado de baja (borrado lógico)."}, status=status.HTTP_200_OK)

@extend_schema_view(
    list=extend_schema(tags=['Pacientes']),
    retrieve=extend_schema(tags=['Pacientes']),
    create=extend_schema(tags=['Pacientes']),
    update=extend_schema(tags=['Pacientes']),
    partial_update=extend_schema(tags=['Pacientes']),
    destroy=extend_schema(tags=['Pacientes']),
)
class PacienteDiagnosticoViewSet(viewsets.ModelViewSet):
    queryset = PacienteDiagnostico.objects.all()
    serializer_class = PacienteDiagnosticoSerializer

@extend_schema_view(
    list=extend_schema(tags=['Pacientes']),
    retrieve=extend_schema(tags=['Pacientes']),
    create=extend_schema(tags=['Pacientes']),
    update=extend_schema(tags=['Pacientes']),
    partial_update=extend_schema(tags=['Pacientes']),
    destroy=extend_schema(tags=['Pacientes']),
)
class ContactoEmergenciaViewSet(viewsets.ModelViewSet):
    queryset = ContactoEmergencia.objects.all()
    serializer_class = ContactoEmergenciaSerializer

@extend_schema_view(
    list=extend_schema(tags=['Sesiones']),
    retrieve=extend_schema(tags=['Sesiones']),
    create=extend_schema(tags=['Sesiones']),
    update=extend_schema(tags=['Sesiones']),
    partial_update=extend_schema(tags=['Sesiones']),
    destroy=extend_schema(tags=['Sesiones']),
)
class SesionViewSet(viewsets.ModelViewSet):
    queryset = Sesion.objects.select_related('paciente', 'terapeuta', 'terapeuta__usuario', 'caballo', 'estatus').all().order_by('-fecha_hora')
    permission_classes = [AllowAny]
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            from api.serializers import SesionWriteSerializer
            return SesionWriteSerializer
        return SesionSerializer

    def create(self, request, *args, **kwargs):
        # REGLA 2: Bienestar Animal
        caballo_id = request.data.get('caballo')
        paciente_id = request.data.get('paciente')
        
        try:
            caballo = Caballo.objects.get(id=caballo_id)
            paciente = Paciente.objects.get(id=paciente_id)
            
            # a) El estado de salud debe ser Activo
            if caballo.estado_salud.nombre.lower() != 'activo':
                return Response({"error": "El caballo no esta en estado Activo."}, status=status.HTTP_400_BAD_REQUEST)
                
            # b) El peso del paciente NO debe superar el peso soportado por el caballo
            if paciente.peso_kg > caballo.peso_max_soporta:
                return Response({"error": "El paciente supera el peso maximo que soporta este caballo."}, status=status.HTTP_400_BAD_REQUEST)
                
        except (Caballo.DoesNotExist, Paciente.DoesNotExist):
            return Response({"error": "Caballo o Paciente no encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

@extend_schema_view(
    list=extend_schema(tags=['Sesiones']),
    retrieve=extend_schema(tags=['Sesiones']),
    create=extend_schema(tags=['Sesiones']),
    update=extend_schema(tags=['Sesiones']),
    partial_update=extend_schema(tags=['Sesiones']),
    destroy=extend_schema(tags=['Sesiones']),
)
class ReporteSesionViewSet(viewsets.ModelViewSet):
    queryset = ReporteSesion.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            from api.serializers import ReporteSesionWriteSerializer
            return ReporteSesionWriteSerializer
        return ReporteSesionSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        try:
            payload = {
                "nombre_paciente": instance.sesion.paciente.nombre,
                "telefono_tutor": instance.sesion.paciente.tutor.telefono,
                "recomendacion_casa": instance.recomendacion_casa,
                "objetivos_trabajados": "N/A"
            }
            print("Webhook disparado a n8n:", payload)
        except Exception as e:
            print("Error disparando webhook:", e)

@extend_schema_view(
    list=extend_schema(tags=['Sesiones']),
    retrieve=extend_schema(tags=['Sesiones']),
    create=extend_schema(tags=['Sesiones']),
    update=extend_schema(tags=['Sesiones']),
    partial_update=extend_schema(tags=['Sesiones']),
    destroy=extend_schema(tags=['Sesiones']),
)
class ReporteObjetivoViewSet(viewsets.ModelViewSet):
    queryset = ReporteObjetivo.objects.all()
    serializer_class = ReporteObjetivoSerializer

@extend_schema_view(
    list=extend_schema(tags=['Pagos']),
    retrieve=extend_schema(tags=['Pagos']),
    create=extend_schema(tags=['Pagos']),
    update=extend_schema(tags=['Pagos']),
    partial_update=extend_schema(tags=['Pagos']),
    destroy=extend_schema(tags=['Pagos']),
)
class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

@extend_schema_view(
    list=extend_schema(tags=['Auditoría']),
    retrieve=extend_schema(tags=['Auditoría']),
)
class BitacoraSeguridadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BitacoraSeguridad.objects.select_related('usuario_afectado', 'usuario_accion').all()
    serializer_class = BitacoraSeguridadSerializer


# ==========================================
# AUTHENTICATION
# ==========================================
@extend_schema(tags=['Usuarios'])
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({"error": "Correo y contraseña son requeridos."}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        user = Usuario.objects.get(email=email)
        if not user.activo:
            # Same generic message to prevent account enumeration
            return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
            
        if check_password(password, user.password):
            # Usar el ID del usuario como token temporal para evitar errores de compatibilidad con DRF Token
            # que requiere que el modelo herede de AbstractUser
            token_key = str(user.id).replace('-', '') 
            return Response({
                "message": "Login exitoso",
                "token": token_key,
                "user": {
                    "id": str(user.id),
                    "nombre": user.nombre_completo,
                    "email": user.email,
                    "rol": user.rol.nombre
                }
            })
        else:
            return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
            
    except Usuario.DoesNotExist:
        # Same message + same status to prevent timing-based enumeration
        return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(tags=['Usuarios'])
@api_view(['POST', 'PUT', 'PATCH'])
def registrar_terapeuta(request, pk=None):
    try:
        # Si hay PK, es una actualización
        if request.method in ['PUT', 'PATCH']:
            terapeuta = Terapeuta.objects.get(id=pk)
            usuario = terapeuta.usuario
            
            # Actualizar Usuario
            usuario.nombre_completo = request.data.get('nombre', usuario.nombre_completo)
            usuario.email = request.data.get('email', usuario.email)
            usuario.telefono = request.data.get('telefono', usuario.telefono)
            if request.data.get('password'):
                usuario.password = make_password(request.data.get('password'))
            usuario.save()

            # Actualizar Terapeuta
            especialidad_id = request.data.get('especialidad_id')
            if especialidad_id:
                terapeuta.especialidad = CatalogoEspecialidad.objects.get(id=especialidad_id)
            
            terapeuta.cedula_profesional = request.data.get('cedula', terapeuta.cedula_profesional)
            terapeuta.biografia = request.data.get('biografia', terapeuta.biografia)
            if 'disponible' in request.data:
                terapeuta.disponible = request.data.get('disponible')
            terapeuta.save()

            return Response({"message": "Terapeuta actualizado exitosamente."})

        # Si no, es creación (código original)
        nombre = request.data.get('nombre')
        email = request.data.get('email')
        telefono = request.data.get('telefono')
        password = request.data.get('password')
        especialidad_id = request.data.get('especialidad_id')
        cedula = request.data.get('cedula', '')
        biografia = request.data.get('biografia', '')

        if Usuario.objects.filter(email=email).exists():
            return Response({"error": "El correo ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)

        rol_terapeuta, _ = Rol.objects.get_or_create(nombre='Terapeuta')
        
        usuario = Usuario.objects.create(
            rol=rol_terapeuta,
            email=email,
            password=make_password(password),
            nombre_completo=nombre,
            telefono=telefono
        )

        especialidad = CatalogoEspecialidad.objects.get(id=especialidad_id)
        terapeuta = Terapeuta.objects.create(
            usuario=usuario,
            especialidad=especialidad,
            cedula_profesional=cedula,
            biografia=biografia
        )

        return Response({"message": "Terapeuta creado exitosamente.", "id": str(terapeuta.id)}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Usuarios'])
@api_view(['POST'])
def resetear_password(request, usuario_id):
    try:
        nueva_password = request.data.get('password')
        if not nueva_password:
            return Response({"error": "Debe proporcionar una nueva contraseña."}, status=status.HTTP_400_BAD_REQUEST)

        usuario = Usuario.objects.get(id=usuario_id)
        usuario.password = make_password(nueva_password)
        usuario.save()

        return Response({"message": "Contraseña actualizada correctamente."})
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(tags=['Pacientes'])
@api_view(['POST'])
def registrar_paciente(request):
    try:
        es_mayor_de_edad = str(request.data.get('es_mayor_de_edad', 'false')).lower() == 'true'
        paciente_nombre = request.data.get('paciente_nombre')
        fecha_nacimiento = request.data.get('fecha_nacimiento')
        peso_kg = request.data.get('peso_kg')
        estado_civil = request.data.get('estado_civil')
        ocupacion_escolaridad = request.data.get('ocupacion_escolaridad')
        direccion = request.data.get('direccion')
        contacto_emergencia = request.data.get('contacto_emergencia')
        motivo_consulta = request.data.get('motivo_consulta')
        historial_medico = request.data.get('historial_medico')
        antecedentes_familiares = request.data.get('antecedentes_familiares')

        tutor_nombre = request.data.get('tutor_nombre')
        tutor_email = request.data.get('tutor_email')
        tutor_telefono = request.data.get('tutor_telefono')
        tutor_password = request.data.get('tutor_password')
        
        tutor2_nombre = request.data.get('tutor2_nombre')
        tutor2_telefono = request.data.get('tutor2_telefono')

        # Convertir peso a float si viene como string
        try:
            if peso_kg:
                peso_kg = float(peso_kg)
        except (ValueError, TypeError):
            peso_kg = 0.0

        if not all([paciente_nombre, fecha_nacimiento]):
            return Response({"error": "Faltan campos obligatorios: nombre y fecha de nacimiento."}, status=status.HTTP_400_BAD_REQUEST)

        if not es_mayor_de_edad and not all([tutor_email]):
            return Response({"error": "Faltan campos obligatorios: email del tutor."}, status=status.HTTP_400_BAD_REQUEST)
        
        if es_mayor_de_edad and not tutor_email:
             return Response({"error": "Debe proporcionar un email para el paciente."}, status=status.HTTP_400_BAD_REQUEST)

        cuenta_email = tutor_email
        cuenta_nombre = paciente_nombre if es_mayor_de_edad else (tutor_nombre or "Tutor de " + paciente_nombre)
        cuenta_telefono = tutor_telefono
        cuenta_password = tutor_password or "cuadra123" # Password por defecto si no viene

        usuario_tutor = Usuario.objects.filter(email=cuenta_email).first()

        if not usuario_tutor:
            nombre_rol = 'Paciente' if es_mayor_de_edad else 'Tutor'
            rol_obj, _ = Rol.objects.get_or_create(nombre=nombre_rol)
            
            usuario_tutor = Usuario.objects.create(
                rol=rol_obj,
                email=cuenta_email,
                password=make_password(cuenta_password),
                nombre_completo=cuenta_nombre,
                telefono=cuenta_telefono
            )

        paciente = Paciente.objects.create(
            tutor=usuario_tutor,
            nombre=paciente_nombre,
            fecha_nacimiento=fecha_nacimiento,
            peso_kg=peso_kg,
            es_mayor_de_edad=es_mayor_de_edad,
            estado_civil=estado_civil,
            ocupacion_escolaridad=ocupacion_escolaridad,
            direccion=direccion,
            contacto_emergencia=contacto_emergencia,
            tutor_secundario_nombre=tutor2_nombre,
            tutor_secundario_telefono=tutor2_telefono,
            motivo_consulta=motivo_consulta,
            historial_medico=historial_medico,
            antecedentes_familiares=antecedentes_familiares
        )

        return Response({
            "message": "Expediente registrado exitosamente.",
            "id": str(paciente.id),
            "paciente": {
                "nombre": paciente.nombre,
                "id": str(paciente.id)
            }
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        import traceback
        print(traceback.format_exc()) # Log para nosotros
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Usuarios'])
@api_view(['PATCH'])
def update_profile(request, usuario_id):
    """Update user profile (name, email, phone)."""
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if request.data.get('nombre_completo'):
            usuario.nombre_completo = request.data['nombre_completo']
        if request.data.get('email'):
            # Check if email is already taken by another user
            existing = Usuario.objects.filter(email=request.data['email']).exclude(id=usuario_id).first()
            if existing:
                return Response({"error": "Este correo ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)
            usuario.email = request.data['email']
        if request.data.get('telefono'):
            usuario.telefono = request.data['telefono']
        usuario.save()
        return Response({
            "message": "Perfil actualizado correctamente.",
            "user": {
                "id": str(usuario.id),
                "nombre": usuario.nombre_completo,
                "email": usuario.email,
                "rol": usuario.rol.nombre
            }
        })
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(tags=['Usuarios'])
@api_view(['POST'])
def change_password(request, usuario_id):
    """Change password with current password verification."""
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response({"error": "Contraseña actual y nueva son requeridas."}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(current_password, usuario.password):
            return Response({"error": "La contraseña actual es incorrecta."}, status=status.HTTP_401_UNAUTHORIZED)

        if len(new_password) < 8:
            return Response({"error": "La nueva contraseña debe tener al menos 8 caracteres."}, status=status.HTTP_400_BAD_REQUEST)

        usuario.password = make_password(new_password)
        usuario.save()

        # Log event
        BitacoraSeguridad.objects.create(
            usuario_afectado=usuario,
            usuario_accion=usuario,
            tipo_evento='PASSWORD_CHANGE',
            descripcion=f"Cambio de contraseña exitoso para el usuario {usuario.email}.",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return Response({"message": "Contraseña actualizada correctamente."})
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(tags=['Auditoría'])
@api_view(['GET'])
def dashboard_stats(request):
    """Returns real stats for the dashboard charts."""
    range_type = request.query_params.get('range', '30') # Default 30 days
    
    now = timezone.now()
    if range_type == '7':
        start_date = now - datetime.timedelta(days=7)
    elif range_type == '30':
        start_date = now - datetime.timedelta(days=30)
    else: # 'all' or others
        start_date = now - datetime.timedelta(days=365)

    # 1. Sesiones por día (Semana actual)
    sesiones_raw = Sesion.objects.filter(fecha_hora__gte=start_date)
    
    # Agrupar por día de la semana (Lunes a Sábado)
    dias_nombres = {0:'Lun', 1:'Mar', 2:'Mié', 3:'Jue', 4:'Vie', 5:'Sáb', 6:'Dom'}
    sesiones_por_dia = []
    for i in range(7):
        date_check = start_date + datetime.timedelta(days=i)
        count = sesiones_raw.filter(fecha_hora__date=date_check.date()).count()
        sesiones_por_dia.append({
            "name": dias_nombres[date_check.weekday()],
            "sesiones": count
        })

    # 2. Crecimiento de Pacientes (Últimos 4 meses)
    pacientes_crecimiento = []
    for i in range(4):
        month_check = (now.month - (3 - i) - 1) % 12 + 1
        year_check = now.year if month_check <= now.month else now.year - 1
        count = Paciente.objects.filter(fecha_registro__month__lte=month_check, fecha_registro__year__lte=year_check).count()
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        pacientes_crecimiento.append({
            "month": meses[month_check - 1],
            "total": count
        })

    # 3. Uso de Caballos (Top 5)
    uso_caballos = Caballo.objects.annotate(
        valor=Count('sesion')
    ).order_by('-valor')[:5].values('nombre', 'valor')
    uso_caballos_list = [{"name": c['nombre'], "valor": c['valor']} for c in uso_caballos]

    # 4. Distribución por Terapeuta
    dist_terapeutas = Terapeuta.objects.annotate(
        value=Count('sesion')
    ).values('usuario__nombre_completo', 'value')
    dist_terapeutas_list = [{"name": t['usuario__nombre_completo'].split(' ')[0], "value": t['value']} for t in dist_terapeutas]

    # --- MÉTRICAS CORE ---
    total_sesiones = Sesion.objects.count()
    total_pacientes = Paciente.objects.filter(activo=True).count()
    total_caballos = Caballo.objects.filter(activo=True).count()
    sesiones_hoy = Sesion.objects.filter(fecha_hora__date=now.date()).count()
    expertos_hoy = Terapeuta.objects.filter(usuario__activo=True, disponible=True).count()

    # --- NUEVAS MÉTRICAS REALES DE SALUD ---
    # A) Disponibilidad Real
    total_staff_activos = Terapeuta.objects.filter(usuario__activo=True).count() + total_caballos
    total_disponibles = expertos_hoy + Caballo.objects.filter(activo=True, disponible=True).count()
    disponibilidad_pct = int((total_disponibles / total_staff_activos * 100)) if total_staff_activos > 0 else 0

    # B) Asistencia Real (Sesiones Finalizadas / Totales pasadas)
    sesiones_pasadas = Sesion.objects.filter(fecha_hora__lte=now).count()
    sesiones_ok = Sesion.objects.filter(estatus__nombre__icontains='Finalizada').count()
    asistencia_pct = int((sesiones_ok / sesiones_pasadas * 100)) if sesiones_pasadas > 0 else 100

    # C) Cumplimiento (Simulado basado en si existen reportes para las sesiones)
    total_reportes = ReporteSesion.objects.count()
    cumplimiento_pct = int((total_reportes / total_sesiones * 100)) if total_sesiones > 0 else 0

    # D) Insight Dinámico
    insight = "La operación está estable. Todo el equipo está respondiendo bien."
    if disponibilidad_pct < 50:
        insight = "Atención: Menos de la mitad de tu equipo está disponible. Revisa las vacaciones."
    elif total_sesiones > 0 and total_reportes < (total_sesiones * 0.5):
        insight = "Aviso: Hay muchas sesiones sin reporte clínico. Los terapeutas deben ponerse al día."
    elif total_pacientes > 20:
        insight = "¡Felicidades! La clínica está creciendo. Considera agregar más caballos."

    return Response({
        "totalSesiones": total_sesiones,
        "totalPacientes": total_pacientes,
        "totalCaballos": total_caballos,
        "sesiones_hoy": sesiones_hoy,
        "expertos_hoy": expertos_hoy,
        "sesionesSemana": sesiones_por_dia,
        "crecimientoPacientes": pacientes_crecimiento,
        "usoCaballos": uso_caballos_list,
        "distribucionTerapeutas": dist_terapeutas_list,
        "salud": {
            "disponibilidad": disponibilidad_pct,
            "asistencia": asistencia_pct,
            "cumplimiento": cumplimiento_pct,
            "insight": insight
        }
    })
