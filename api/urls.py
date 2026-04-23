from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    RoleViewSet, CaballoEstadoSaludViewSet, EstatusSesionViewSet,
    EstadosPagoViewSet, ParentescoViewSet, DiagnosticosViewSet,
    ObjetivosViewSet, UsuarioViewSet, TutorViewSet, TerapeutasViewSet,
    CaballoViewSet, PacienteViewSet, ContactosEmergenciaViewSet,
    PacientesDiagnosticosViewSet, SesionViewSet, ReporteSesionViewSet,
    ReporteObjetivosViewSet, BitacoraEquinaViewSet, PagosViewSet
)

# Crear router y registrar todos los ViewSets
router = DefaultRouter()

# Catálogos
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'caballo-estado-salud', CaballoEstadoSaludViewSet, basename='caballo-estado-salud')
router.register(r'estatus-sesion', EstatusSesionViewSet, basename='estatus-sesion')
router.register(r'estados-pago', EstadosPagoViewSet, basename='estados-pago')
router.register(r'parentescos', ParentescoViewSet, basename='parentesco')
router.register(r'diagnosticos', DiagnosticosViewSet, basename='diagnosticos')
router.register(r'objetivos', ObjetivosViewSet, basename='objetivos')

# Usuarios
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'tutores', TutorViewSet, basename='tutor')
router.register(r'terapeutas', TerapeutasViewSet, basename='terapeuta')

# Caballos
router.register(r'caballos', CaballoViewSet, basename='caballo')

# Pacientes
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'contactos-emergencia', ContactosEmergenciaViewSet, basename='contacto-emergencia')
router.register(r'pacientes-diagnosticos', PacientesDiagnosticosViewSet, basename='paciente-diagnostico')

# Sesiones
router.register(r'sesiones', SesionViewSet, basename='sesion')
router.register(r'reportes-sesion', ReporteSesionViewSet, basename='reporte-sesion')
router.register(r'reportes-objetivos', ReporteObjetivosViewSet, basename='reporte-objetivo')

# Bitácoras y Pagos
router.register(r'bitacoras-equinas', BitacoraEquinaViewSet, basename='bitacora-equina')
router.register(r'pagos', PagosViewSet, basename='pago')

urlpatterns = [
    path('', include(router.urls)),
]
