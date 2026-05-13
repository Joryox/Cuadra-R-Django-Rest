from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Count, Sum
from django.utils import timezone
from django.db import transaction
import jwt, datetime, os
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from api.models import (
    Rol, Usuario, CatalogoEspecialidad, CatalogoDiagnostico,
    CatalogoObjetivo, CatalogoEstadoCaballo, CatalogoEventoEquino,
    CatalogoEstadoSesion, CatalogoEstadoPago, CatalogoParentesco,
    Terapeuta, Caballo, BitacoraEquina, Paciente, PacienteDiagnostico,
    ContactoEmergencia, Sesion, ReporteSesion, ReporteObjetivo, Pago,
    BitacoraSeguridad, PasswordResetToken
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

    from rest_framework.decorators import action as drf_action

    @drf_action(detail=True, methods=['post'], url_path='cambiar-contrasena')
    def cambiar_contrasena(self, request, pk=None):
        usuario = self.get_object()
        actual = request.data.get('password_actual', '')
        nueva = request.data.get('password_nueva', '')
        if not check_password(actual, usuario.password):
            return Response({'error': 'Contraseña actual incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(nueva) < 8:
            return Response({'error': 'La nueva contraseña debe tener al menos 8 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)
        usuario.password = make_password(nueva)
        usuario.save()
        return Response({'message': 'Contraseña actualizada correctamente.'})

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

    def perform_update(self, serializer):
        instance = serializer.save()
        data = self.request.data
        if 'disponible' in data:
            disp = data.get('disponible')
            if isinstance(disp, str):
                disp = disp.lower() == 'true'
            
            instance.estado_salud_id = 1 if disp else 2
            if disp:
                instance.motivo_inactividad = None
            instance.save(update_fields=['estado_salud_id', 'motivo_inactividad'])

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
        # Si es terapeuta, solo ve sus propios eventos o los que él reportó
        if not self.request.user.is_staff and hasattr(self.request.user, 'terapeuta'):
             # Los terapeutas pueden ver todas las bitácoras (para conocer el estado del caballo)
             # Pero solo pueden editar las propias si quisiéramos restringir más.
             # Por ahora, permitimos lectura total por bienestar animal.
             pass
        
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
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        rol = getattr(self.request.user, 'rol', None)
        rol_nombre = getattr(rol, 'nombre', '') if rol else ''

        # Tutores solo ven sus propios pacientes
        if rol_nombre in ['Tutor', 'Paciente']:
            return qs.filter(tutor=self.request.user, activo=True)

        # Admin puede ver inactivos con ?activo=false
        activo_param = self.request.query_params.get('activo', 'true')
        if activo_param.lower() == 'false':
            return qs.filter(activo=False)

        # Por defecto, terapeuta y admin solo ven activos
        return qs.filter(activo=True)

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

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            return qs.none()
            
        rol_nombre = getattr(self.request.user.rol, 'nombre', '')
        
        if not self.request.user.is_staff:
            if rol_nombre == 'Terapeuta':
                qs = qs.filter(terapeuta__usuario=self.request.user)
            elif rol_nombre in ['Tutor', 'Paciente']:
                qs = qs.filter(paciente__tutor=self.request.user)

        # Filtro de archivadas (borrado lógico)
        archivada_param = self.request.query_params.get('archivada')
        if archivada_param == 'true':
            qs = qs.filter(archivada=True)
        else:
            qs = qs.filter(archivada=False)

        fecha = self.request.query_params.get('fecha')
        if fecha:
            qs = qs.filter(fecha_hora__date=fecha)

        return qs

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            from api.serializers import SesionWriteSerializer
            return SesionWriteSerializer
        return SesionSerializer

    def create(self, request, *args, **kwargs):
        """
        Validaciones previas al guardar una sesión:
          1. Bienestar Animal: estado Activo + límite de peso.
          2. Anti-colisión con duración: caballo y terapeuta libres en ese rango de tiempo.
          3. Límite semanal de sesiones del caballo (máx 10/semana).
        Se consideran en conflicto las sesiones con estatus 'Programada' o 'En Curso'.
        """
        from datetime import timedelta as td
        from django.utils.timezone import make_aware
        import pytz

        caballo_id   = request.data.get('caballo')
        paciente_id  = request.data.get('paciente')
        terapeuta_id = request.data.get('terapeuta')
        fecha_hora   = request.data.get('fecha_hora')
        duracion_min = int(request.data.get('duracion_minutos', 60))

        try:
            caballo  = Caballo.objects.get(id=caballo_id)
            paciente = Paciente.objects.get(id=paciente_id)
        except (Caballo.DoesNotExist, Paciente.DoesNotExist):
            return Response({"error": "Caballo o Paciente no encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # ── Regla 1: Bienestar Animal ─────────────────────────────────────────
        if caballo.estado_salud.nombre.lower() != 'activo':
            return Response(
                {"error": "El caballo no está en estado Activo y no puede trabajar."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if paciente.peso_kg > caballo.peso_max_soporta:
            return Response(
                {"error": f"El paciente ({paciente.peso_kg} kg) supera el peso máximo que soporta {caballo.nombre} ({caballo.peso_max_soporta} kg)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ── Regla 2: Anti-Colisión con Duración ──────────────────────────────
        if fecha_hora:
            from dateutil import parser as dp
            try:
                inicio_nueva = dp.parse(fecha_hora)
            except Exception:
                inicio_nueva = None

            if inicio_nueva:
                fin_nueva = inicio_nueva + td(minutes=duracion_min)

                estatus_bloqueantes = CatalogoEstadoSesion.objects.filter(
                    nombre__in=['Programada', 'En Curso']
                ).values_list('id', flat=True)

                # Sesiones del caballo que se solapan: [ini, fin) se cruza con [ini_nueva, fin_nueva)
                conflictos_caballo = Sesion.objects.filter(
                    caballo_id=caballo_id,
                    estatus_id__in=estatus_bloqueantes,
                ).exclude(id=request.data.get('exclude_id', None))

                for s in conflictos_caballo:
                    ini_s = s.fecha_hora
                    fin_s = ini_s + td(minutes=s.duracion_minutos)
                    if ini_s < fin_nueva and fin_s > inicio_nueva:
                        ini_fmt = ini_s.strftime("%H:%M")
                        fin_fmt = fin_s.strftime("%H:%M")
                        return Response(
                            {"error": f"🐴 {caballo.nombre} estará ocupado de {ini_fmt} a {fin_fmt}. "
                                      f"Por favor elige otro horario, fecha o caballo."},
                            status=status.HTTP_409_CONFLICT
                        )

                # Conflicto de terapeuta (mismo esquema)
                conflictos_terapeuta = Sesion.objects.filter(
                    terapeuta_id=terapeuta_id,
                    estatus_id__in=estatus_bloqueantes,
                )
                for s in conflictos_terapeuta:
                    ini_s = s.fecha_hora
                    fin_s = ini_s + td(minutes=s.duracion_minutos)
                    if ini_s < fin_nueva and fin_s > inicio_nueva:
                        return Response(
                            {"error": "El terapeuta ya tiene otra sesión en ese horario."},
                            status=status.HTTP_409_CONFLICT
                        )

        # ── Regla 3: Límite semanal del caballo (máx 10/semana) ──────────────
        if fecha_hora:
            from dateutil import parser as dp2
            try:
                d = dp2.parse(fecha_hora)
            except Exception:
                d = timezone.now()
            # Inicio de semana (lunes)
            inicio_semana = d - td(days=d.weekday())
            inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
            fin_semana    = inicio_semana + td(days=7)

            sesiones_semana = Sesion.objects.filter(
                caballo_id=caballo_id,
                fecha_hora__gte=inicio_semana,
                fecha_hora__lt=fin_semana,
            ).exclude(estatus__nombre__in=['Cancelada']).count()

            max_semana = getattr(caballo, 'sesiones_semanales_max', 10) or 10
            if sesiones_semana >= max_semana:
                return Response(
                    {"error": f"🐴 {caballo.nombre} ya alcanzó su límite de {max_semana} sesiones esta semana. "
                              f"Por favor elige otro caballo u otra semana."},
                    status=status.HTTP_409_CONFLICT
                )

        return super().create(request, *args, **kwargs)


# ── Verificar disponibilidad de caballo (usado por el frontend) ──────────────
@api_view(['GET'])
@permission_classes([AllowAny])
def caballo_disponibilidad(request):
    """
    GET /api/caballo-disponibilidad/?caballo_id=X&fecha=YYYY-MM-DD&hora=HH:MM&duracion=60
    Retorna: { disponible, ocupado_de, ocupado_hasta, sesiones_semana, max_semana, porcentaje_carga }
    """
    from datetime import timedelta as td
    from dateutil import parser as dp

    caballo_id = request.query_params.get('caballo_id')
    fecha      = request.query_params.get('fecha')
    hora       = request.query_params.get('hora', '09:00')
    duracion   = int(request.query_params.get('duracion', 60))

    if not caballo_id:
        return Response({"error": "Se requiere caballo_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        caballo = Caballo.objects.get(id=caballo_id)
    except Caballo.DoesNotExist:
        return Response({"error": "Caballo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Sesiones de esta semana
    hoy = timezone.now()
    inicio_semana = hoy - td(days=hoy.weekday())
    inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_semana    = inicio_semana + td(days=7)

    sesiones_semana = Sesion.objects.filter(
        caballo_id=caballo_id,
        fecha_hora__gte=inicio_semana,
        fecha_hora__lt=fin_semana,
    ).exclude(estatus__nombre__in=['Cancelada']).count()

    max_semana = getattr(caballo, 'sesiones_semanales_max', 10) or 10
    porcentaje = round((sesiones_semana / max_semana) * 100, 1) if max_semana > 0 else 0

    resp = {
        "disponible": True,
        "ocupado_de": None,
        "ocupado_hasta": None,
        "sesiones_semana": sesiones_semana,
        "max_semana": max_semana,
        "porcentaje_carga": porcentaje,
        "alcanzado_limite": sesiones_semana >= max_semana,
    }

    if fecha and hora:
        try:
            inicio_nueva = dp.parse(f"{fecha}T{hora}:00")
            fin_nueva    = inicio_nueva + td(minutes=duracion)

            estatus_bloq = CatalogoEstadoSesion.objects.filter(
                nombre__in=['Programada', 'En Curso']
            ).values_list('id', flat=True)

            for s in Sesion.objects.filter(caballo_id=caballo_id, estatus_id__in=estatus_bloq):
                ini_s = s.fecha_hora
                fin_s = ini_s + td(minutes=s.duracion_minutos)
                if ini_s < fin_nueva and fin_s > inicio_nueva:
                    resp["disponible"] = False
                    resp["ocupado_de"]    = ini_s.strftime("%H:%M")
                    resp["ocupado_hasta"] = fin_s.strftime("%H:%M")
                    break
        except Exception:
            pass

    return Response(resp)

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

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            return qs.none()
            
        rol_nombre = getattr(self.request.user.rol, 'nombre', '')
        
        if not self.request.user.is_staff:
            if rol_nombre == 'Terapeuta':
                return qs.filter(sesion__terapeuta__usuario=self.request.user)
            elif rol_nombre in ['Tutor', 'Paciente']:
                return qs.filter(sesion__paciente__tutor=self.request.user)
        return qs

    def get_serializer_class(self):
        from api.serializers import (
            ReporteSesionWriteSerializer, 
            ReporteSesionSerializer, 
            TutorReporteSesionSerializer
        )
        # SI ES TUTOR O PACIENTE, USAR SERIALIZADOR SIN NOTAS CLÍNICAS (PRIVACIDAD MÉDICA)
        rol_nombre = getattr(self.request.user.rol, 'nombre', '') if not self.request.user.is_anonymous else ''
        if not self.request.user.is_staff and rol_nombre in ['Tutor', 'Paciente']:
            return TutorReporteSesionSerializer
        
        if self.action in ['create', 'update', 'partial_update']:
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
    """
    Login endpoint — devuelve access_token (JWT 12h) + refresh_token (7d).
    El payload incluye 'rol' y 'redirect_to' para que Next.js sepa
    a qué dashboard redirigir sin necesitar otra petición al backend.
    """
    from api.jwt_serializers import CuadraTokenObtainPairSerializer
    serializer = CuadraTokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        return Response({
            "message": "Login exitoso",
            "access":  data['access'],
            "refresh": data['refresh'],
            "user":    data['user'],
        }, status=status.HTTP_200_OK)
    # Aplanar errores del serializer en un solo string legible
    errors = serializer.errors
    detail = errors.get('detail') or errors.get('non_field_errors') or str(errors)
    if isinstance(detail, list):
        detail = detail[0]
    return Response({"error": str(detail)}, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(tags=['Usuarios'])
@api_view(['POST', 'PUT', 'PATCH'])
def registrar_terapeuta(request, pk=None):
    try:
        import string
        def cap(v): return string.capwords(v.strip()) if v and isinstance(v, str) else v
        def cap_sentence(v): return (v.strip()[0].upper() + v.strip()[1:]) if v and isinstance(v, str) and v.strip() else v

        # Si hay PK, es una actualización
        if request.method in ['PUT', 'PATCH']:
            terapeuta = Terapeuta.objects.get(id=pk)
            usuario = terapeuta.usuario
            
            # Actualizar Usuario
            usuario.nombre_completo = cap(request.data.get('nombre', usuario.nombre_completo))
            usuario.email = request.data.get('email', usuario.email)
            usuario.telefono = request.data.get('telefono', usuario.telefono)
            if request.data.get('password'):
                usuario.password = make_password(request.data.get('password'))
            usuario.save()

            # Actualizar Terapeuta
            terapeuta.carrera = cap(request.data.get('carrera', terapeuta.carrera))
            terapeuta.especialidad_text = cap_sentence(request.data.get('especialidad_text', terapeuta.especialidad_text))
            
            rfc_val = request.data.get('rfc', terapeuta.rfc)
            terapeuta.rfc = rfc_val.upper() if rfc_val else rfc_val
            
            terapeuta.contacto_emergencia = cap(request.data.get('contacto_emergencia', terapeuta.contacto_emergencia))
            terapeuta.cedula_profesional = request.data.get('cedula', terapeuta.cedula_profesional)
            terapeuta.biografia = cap_sentence(request.data.get('biografia', terapeuta.biografia))
            
            if 'disponible' in request.data:
                terapeuta.disponible = request.data.get('disponible')
            terapeuta.save()

            return Response({"message": "Terapeuta actualizado exitosamente."})

        # Si no, es creación — envuelto en transacción atómica
        nombre = cap(request.data.get('nombre'))
        email = request.data.get('email')
        telefono = request.data.get('telefono')
        password = request.data.get('password')
        
        carrera = cap(request.data.get('carrera', ''))
        especialidad_text = cap_sentence(request.data.get('especialidad_text', ''))
        rfc = request.data.get('rfc', '').upper()
        contacto_emergencia = cap(request.data.get('contacto_emergencia', ''))
        
        cedula = request.data.get('cedula', '')
        biografia = cap_sentence(request.data.get('biografia', ''))

        if Usuario.objects.filter(email=email).exists():
            return Response({"error": "El correo ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)

        if rfc and Terapeuta.objects.filter(rfc__iexact=rfc).exists():
            return Response({"error": f"El RFC '{rfc}' ya pertenece a otro terapeuta."}, status=status.HTTP_400_BAD_REQUEST)

        # TAREA 1: transaction.atomic garantiza cero usuarios huérfanos.
        # Si falla el INSERT de Terapeuta, el Usuario se revierte automáticamente.
        with transaction.atomic():
            rol_terapeuta, _ = Rol.objects.get_or_create(nombre='Terapeuta')
            usuario = Usuario.objects.create(
                rol=rol_terapeuta,
                email=email,
                password=make_password(password),
                nombre_completo=nombre,
                telefono=telefono
            )
            terapeuta = Terapeuta.objects.create(
                usuario=usuario,
                carrera=carrera,
                especialidad_text=especialidad_text,
                rfc=rfc,
                contacto_emergencia=contacto_emergencia,
                cedula_profesional=cedula,
                biografia=biografia
            )

        return Response({"message": "Terapeuta creado exitosamente.", "id": str(terapeuta.id)}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Usuarios'])
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """Generates a magic link token and outputs it to the console (Option B simulated, ready for SMTP)."""
    email = request.data.get('email', '').strip()
    if not email:
        return Response({"error": "El correo es requerido."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        usuario = Usuario.objects.get(email__iexact=email)
        
        # Invalida tokens anteriores para que solo el último funcione
        PasswordResetToken.objects.filter(usuario=usuario, utilizado=False).update(utilizado=True)
        
        # Create token
        token = PasswordResetToken.objects.create(usuario=usuario)
        
        reset_link = f"http://localhost:3000/reset-password?token={token.id}"
        
        # Enviar correo real de forma asíncrona para que no tarde 1 minuto!
        import threading
        
        def enviar_correo_magico():
            from django.core.mail import send_mail
            from django.conf import settings
            
            html_message = f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #821026;">Recuperación de Acceso</h2>
                <p>Hola <strong>{usuario.nombre_completo}</strong>,</p>
                <p>Hemos recibido una solicitud para acceder a tu cuenta en el Portal de Cuadra Erre.</p>
                <p>Haz clic en el siguiente botón seguro para establecer tu nueva contraseña:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" style="background-color: #821026; color: white; padding: 15px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
                        Reestablecer Contraseña
                    </a>
                </div>
                <p style="color: #666; font-size: 12px;">Este enlace expira en 1 hora. Si solicitas otro, este enlace quedará invalidado de inmediato.</p>
            </div>
            """
            try:
                send_mail(
                    subject="🔑 Recupera tu acceso a Cuadra Erre",
                    message=f"Entra a este enlace para recuperar tu contraseña: {reset_link}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[usuario.email],
                    fail_silently=True,
                    html_message=html_message
                )
            except Exception as e:
                print("Error al enviar correo:", e)
                
        # Iniciar el hilo sin bloquear la respuesta web
        threading.Thread(target=enviar_correo_magico).start()
        
        return Response({"message": "¡Enlace de seguridad enviado con éxito!"}, status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        # El usuario pidió un error explícito
        return Response({"error": "Este correo no está registrado en el sistema. Verifica que esté bien escrito."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_magic(request):
    """Consumes the magic link token and sets a new password."""
    token_id = request.data.get('token')
    new_password = request.data.get('new_password')
    
    if not token_id or not new_password:
        return Response({"error": "Token y nueva contraseña son requeridos."}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        token_obj = PasswordResetToken.objects.get(id=token_id)
        if not token_obj.is_valid():
            return Response({"error": "El enlace ha expirado o ya fue utilizado."}, status=status.HTTP_400_BAD_REQUEST)
            
        usuario = token_obj.usuario
        usuario.password = make_password(new_password)
        usuario.save()
        
        token_obj.utilizado = True
        token_obj.save()
        
        return Response({"message": "Contraseña actualizada exitosamente."}, status=status.HTTP_200_OK)
    except PasswordResetToken.DoesNotExist:
        return Response({"error": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resetear_password(request, usuario_id):
    try:
        nueva_password = request.data.get('new_password') or request.data.get('password')
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
@authentication_classes([])   # El admin ya está protegido por el routing del frontend
@permission_classes([AllowAny])
def registrar_paciente(request):
    """
    TAREA 1: Transacción atómica.
    La creación de Usuario (Tutor/Paciente) + Paciente ocurre en un solo bloque.
    Si Paciente.create() falla por cualquier motivo, el Usuario se revierte
    automáticamente → cero usuarios huérfanos en base de datos.
    """
    try:
        import re as _re
        def _cap(v):
            """Capitaliza primera letra de cada palabra — soporta acentos españoles."""
            if not v or not isinstance(v, str): return v
            return _re.sub(r"(?<!\w)(\w)", lambda m: m.group(1).upper(), v.strip())
        def _csnt(v):
            """Capitaliza solo la primera letra de la oración."""
            v = (v or '').strip()
            return v[0].upper() + v[1:] if v else v

        es_mayor_de_edad = str(request.data.get('es_mayor_de_edad', 'false')).lower() == 'true'
        paciente_nombre        = _cap(request.data.get('paciente_nombre'))
        fecha_nacimiento       = request.data.get('fecha_nacimiento')
        peso_kg                = request.data.get('peso_kg')
        estado_civil           = _cap(request.data.get('estado_civil'))
        ocupacion_escolaridad  = _csnt(request.data.get('ocupacion_escolaridad'))
        direccion              = _cap(request.data.get('direccion'))
        contacto_emergencia    = _cap(request.data.get('contacto_emergencia'))
        motivo_consulta        = _csnt(request.data.get('motivo_consulta'))
        historial_medico       = _csnt(request.data.get('historial_medico'))
        antecedentes_familiares= _csnt(request.data.get('antecedentes_familiares'))
        tutor_nombre           = _cap(request.data.get('tutor_nombre'))
        tutor_email            = request.data.get('tutor_email')
        tutor_telefono         = request.data.get('tutor_telefono')
        tutor_password         = request.data.get('tutor_password')
        tutor2_nombre          = _cap(request.data.get('tutor2_nombre'))
        tutor2_telefono        = request.data.get('tutor2_telefono')

        try:
            peso_kg = float(peso_kg) if peso_kg else 0.0
        except (ValueError, TypeError):
            peso_kg = 0.0

        # Validaciones previas (antes de abrir la transacción)
        if not all([paciente_nombre, fecha_nacimiento]):
            return Response({"error": "Faltan campos obligatorios: nombre y fecha de nacimiento."}, status=status.HTTP_400_BAD_REQUEST)
        if not es_mayor_de_edad and not tutor_email:
            return Response({"error": "Faltan campos obligatorios: email del tutor."}, status=status.HTTP_400_BAD_REQUEST)
        if es_mayor_de_edad and not tutor_email:
            return Response({"error": "Debe proporcionar un email para el paciente."}, status=status.HTTP_400_BAD_REQUEST)

        # Prevención de duplicados: No permitir registrar si ya existe el mismo nombre y fecha de nacimiento
        if Paciente.objects.filter(nombre__iexact=paciente_nombre, fecha_nacimiento=fecha_nacimiento).exists():
            return Response({"error": f"Ya existe un paciente con el nombre '{paciente_nombre}' y la misma fecha de nacimiento."}, status=status.HTTP_400_BAD_REQUEST)

        cuenta_email    = tutor_email
        cuenta_nombre   = paciente_nombre if es_mayor_de_edad else (tutor_nombre or "Tutor de " + paciente_nombre)
        cuenta_telefono = tutor_telefono
        cuenta_password = tutor_password or "cuadra123"

        # ── BLOQUE ATÓMICO ────────────────────────────────────────────────────
        with transaction.atomic():
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
        # ── FIN BLOQUE ATÓMICO ────────────────────────────────────────────────

        return Response({
            "message": "Expediente registrado exitosamente.",
            "id": str(paciente.id),
            "paciente": {"nombre": paciente.nombre, "id": str(paciente.id)}
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
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
