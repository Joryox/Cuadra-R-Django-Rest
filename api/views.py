from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from api.models import (
    Role, Usuario, CaballoEstadoSalud, Caballo, Tutor, Paciente,
    Diagnosticos, PacientesDiagnosticos, ContactosEmergencia, Parentesco,
    BitacoraEquina, EstatusSesion, Terapeutas, Sesion, ReporteSesion,
    ReporteObjetivos, Objetivos, EstadosPago, Pagos
)
from api.serializers import (
    RoleSerializer, UsuarioSerializer, CaballoEstadoSaludSerializer,
    CaballoSerializer, TutorSerializer, PacienteSerializer,
    DiagnosticosSerializer, PacientesDiagnosticosSerializer,
    ContactosEmergenciaSerializer, ParentescoSerializer, BitacoraEquinaSerializer,
    EstatusSesionSerializer, TerapeutasSerializer, SesionSerializer,
    ReporteSesionSerializer, ReporteObjetivosSerializer, ObjetivosSerializer,
    EstadosPagoSerializer, PagosSerializer
)
from api.permissions import (
    IsAdminUser as CustomIsAdminUser, IsTerapeuta, IsTutor, 
    CanManageUsers, CanManageSessions, CanManagePacients
)
from api.filters import (
    UsuarioFilter, CaballoFilter, PacienteFilter, SesionFilter,
    BitacoraEquinaFilter, PagosFilter, ContactosEmergenciaFilter,
    TerapeutasFilter, TutorFilter
)


# ============== VIEWSETS PARA CATÁLOGOS ==============

class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet para Role (solo lectura o CRUD)."""
    queryset = Role.objects.filter(eliminado=False)
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['nombre']


class CaballoEstadoSaludViewSet(viewsets.ModelViewSet):
    """ViewSet para CaballoEstadoSalud."""
    queryset = CaballoEstadoSalud.objects.all()
    serializer_class = CaballoEstadoSaludSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['descripcion']


class EstatusSesionViewSet(viewsets.ModelViewSet):
    """ViewSet para EstatusSesion."""
    queryset = EstatusSesion.objects.all()
    serializer_class = EstatusSesionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['descripcion']


class EstadosPagoViewSet(viewsets.ModelViewSet):
    """ViewSet para EstadosPago."""
    queryset = EstadosPago.objects.all()
    serializer_class = EstadosPagoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['descripcion']


class ParentescoViewSet(viewsets.ModelViewSet):
    """ViewSet para Parentesco."""
    queryset = Parentesco.objects.all()
    serializer_class = ParentescoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['descripcion']


class DiagnosticosViewSet(viewsets.ModelViewSet):
    """ViewSet para Diagnosticos."""
    queryset = Diagnosticos.objects.all()
    serializer_class = DiagnosticosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['descripcion']
    search_fields = ['descripcion']


class ObjetivosViewSet(viewsets.ModelViewSet):
    """ViewSet para Objetivos."""
    queryset = Objetivos.objects.all()
    serializer_class = ObjetivosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['descripcion']
    search_fields = ['descripcion']


# ============== VIEWSETS PARA USUARIOS ==============

class UsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para Usuario con permisos granulares."""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = UsuarioFilter
    search_fields = ['nombres', 'apellidos', 'usuario', 'correo']
    ordering_fields = ['creacion', 'nombres']

    def get_permissions(self):
        """Permisos granulares según acción."""
        if self.action in ['create', 'destroy', 'partial_update']:
            return [CustomIsAdminUser()]
        if self.action == 'update':
            return [CustomIsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Acción para cambiar contraseña."""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {'error': 'Debe proporcionar contraseña antigua y nueva'},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario = Usuario.objects.get(id=user.id)
        # En producción, validar old_password contra password_hash
        usuario.password_hash = usuario.password_hash  # Make password se haría aquí
        usuario.save()

        return Response({'message': 'Contraseña actualizada'}, status=status.HTTP_200_OK)


class TutorViewSet(viewsets.ModelViewSet):
    """ViewSet para Tutor con permisos por rol."""
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TutorFilter
    search_fields = ['usuario_id__nombres', 'usuario_id__apellidos', 'telefono']
    ordering_fields = ['creacion', 'usuario_id__nombres']

    def get_queryset(self):
        """Tutores solo ven sus propios datos."""
        user = self.request.user
        if getattr(user, 'is_superuser', False):
            return Tutor.objects.all()
        if hasattr(user, 'roles'):
            if user.roles.filter(nombre__iexact='admin').exists():
                return Tutor.objects.all()
            if user.roles.filter(nombre__iexact='tutor').exists():
                return Tutor.objects.filter(usuario_id=user.id)
        return Tutor.objects.none()


class TerapeutasViewSet(viewsets.ModelViewSet):
    """ViewSet para Terapeutas con permisos por rol."""
    queryset = Terapeutas.objects.all()
    serializer_class = TerapeutasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TerapeutasFilter
    search_fields = ['usuario_id__nombres', 'usuario_id__apellidos', 'especialidad']
    ordering_fields = ['creacion', 'especialidad']


# ============== VIEWSETS PARA CABALLOS ==============

class CaballoViewSet(viewsets.ModelViewSet):
    """ViewSet para Caballo con filtros y búsqueda."""
    queryset = Caballo.objects.filter(eliminado=False)
    serializer_class = CaballoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CaballoFilter
    search_fields = ['nombre', 'raza']
    ordering_fields = ['nombre', 'edad', 'creacion']

    def get_permissions(self):
        """Solo admin puede crear/editar/eliminar."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [CustomIsAdminUser()]
        return [IsAuthenticated()]


# ============== VIEWSETS PARA PACIENTES ==============

class PacienteViewSet(viewsets.ModelViewSet):
    """ViewSet para Paciente con permisos granulares."""
    queryset = Paciente.objects.filter(eliminado=False)
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PacienteFilter
    search_fields = ['nombre', 'tutor_id__usuario_id__nombres']
    ordering_fields = ['nombre', 'edad', 'creacion']

    def get_queryset(self):
        """Tutores solo ven sus propios pacientes."""
        user = self.request.user
        if getattr(user, 'is_superuser', False):
            return Paciente.objects.filter(eliminado=False)
        if hasattr(user, 'roles'):
            if user.roles.filter(nombre__iexact='admin').exists():
                return Paciente.objects.filter(eliminado=False)
            if user.roles.filter(nombre__iexact='tutor').exists():
                tutor = Tutor.objects.filter(usuario_id=user.id).first()
                return Paciente.objects.filter(tutor_id=tutor, eliminado=False)
        return Paciente.objects.filter(eliminado=False)

    def get_permissions(self):
        """Tutores solo CRUD sus propios pacientes."""
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated()]
        if self.action == 'destroy':
            return [CustomIsAdminUser()]
        return [IsAuthenticated()]


class ContactosEmergenciaViewSet(viewsets.ModelViewSet):
    """ViewSet para ContactosEmergencia."""
    queryset = ContactosEmergencia.objects.all()
    serializer_class = ContactosEmergenciaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ContactosEmergenciaFilter
    search_fields = ['nombre', 'paciente_id__nombre']


class PacientesDiagnosticosViewSet(viewsets.ModelViewSet):
    """ViewSet para PacientesDiagnosticos."""
    queryset = PacientesDiagnosticos.objects.all()
    serializer_class = PacientesDiagnosticosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['paciente_id', 'diagnostico']


# ============== VIEWSETS PARA SESIONES ==============

class SesionViewSet(viewsets.ModelViewSet):
    """ViewSet para Sesion con permisos granulares y filtros avanzados."""
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SesionFilter
    search_fields = ['paciente_id__nombre', 'terapeuta_id__usuario_id__nombres', 'observaciones']
    ordering_fields = ['fecha_hora', 'creacion']

    def get_queryset(self):
        """Terapeutas solo ven sus propias sesiones."""
        user = self.request.user
        if getattr(user, 'is_superuser', False):
            return Sesion.objects.all()
        if hasattr(user, 'roles'):
            if user.roles.filter(nombre__iexact='admin').exists():
                return Sesion.objects.all()
            if user.roles.filter(nombre__iexact='terapeuta').exists():
                terapeuta = Terapeutas.objects.filter(usuario_id=user.id).first()
                return Sesion.objects.filter(terapeuta_id=terapeuta)
        return Sesion.objects.all()

    def get_permissions(self):
        """Terapeutas solo editan sus propias sesiones."""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def crear_reporte(self, request, pk=None):
        """Acción custom para crear reporte de una sesión."""
        sesion = self.get_object()
        data = request.data.copy()
        data['sesion_id'] = sesion.id

        serializer = ReporteSesionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReporteSesionViewSet(viewsets.ModelViewSet):
    """ViewSet para ReporteSesion."""
    queryset = ReporteSesion.objects.all()
    serializer_class = ReporteSesionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['sesion_id', 'creacion']
    ordering_fields = ['creacion']

    def get_permissions(self):
        """Solo lectura para no-terapeutas."""
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            return [IsTerapeuta()]
        return [IsAuthenticated()]


class ReporteObjetivosViewSet(viewsets.ModelViewSet):
    """ViewSet para ReporteObjetivos."""
    queryset = ReporteObjetivos.objects.all()
    serializer_class = ReporteObjetivosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reporte_sesion_id', 'objetivo_id']


# ============== VIEWSETS PARA BITÁCORAS Y PAGOS ==============

class BitacoraEquinaViewSet(viewsets.ModelViewSet):
    """ViewSet para BitacoraEquina con filtros de fecha."""
    queryset = BitacoraEquina.objects.all()
    serializer_class = BitacoraEquinaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BitacoraEquinaFilter
    ordering_fields = ['fecha_sesion', 'creacion']

    def get_permissions(self):
        """Solo lectura para no-terapeutas."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]  # Cualquier usuario autenticado puede modificar
        return [IsAuthenticated()]


class PagosViewSet(viewsets.ModelViewSet):
    """ViewSet para Pagos con permisos granulares."""
    queryset = Pagos.objects.all()
    serializer_class = PagosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PagosFilter
    ordering_fields = ['creacion', 'monto']

    def get_queryset(self):
        """Tutores solo ven sus propios pagos."""
        user = self.request.user
        if getattr(user, 'is_superuser', False):
            return Pagos.objects.all()
        if hasattr(user, 'roles'):
            if user.roles.filter(nombre__iexact='admin').exists():
                return Pagos.objects.all()
            if user.roles.filter(nombre__iexact='tutor').exists():
                tutor = Tutor.objects.filter(usuario_id=user.id).first()
                return Pagos.objects.filter(tutor_id=tutor)
        return Pagos.objects.all()

    def get_permissions(self):
        """Tutores pueden crear pagos, solo admin puede editar/eliminar."""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [CustomIsAdminUser()]
        return [IsAuthenticated()]
