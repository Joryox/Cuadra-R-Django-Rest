from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import *

router = DefaultRouter()

# Catálogos
router.register(r'roles', RolViewSet)
router.register(r'especialidades', CatalogoEspecialidadViewSet)
router.register(r'diagnosticos', CatalogoDiagnosticoViewSet)
router.register(r'objetivos', CatalogoObjetivoViewSet)
router.register(r'estados-caballo', CatalogoEstadoCaballoViewSet)
router.register(r'eventos-equinos', CatalogoEventoEquinoViewSet)
router.register(r'estados-sesion', CatalogoEstadoSesionViewSet)
router.register(r'estados-pago', CatalogoEstadoPagoViewSet)
router.register(r'parentescos', CatalogoParentescoViewSet)

# Core
router.register(r'usuarios', UsuarioViewSet)
router.register(r'terapeutas', TerapeutaViewSet)
router.register(r'caballos', CaballoViewSet)
router.register(r'bitacoras-equinas', BitacoraEquinaViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'pacientes-diagnosticos', PacienteDiagnosticoViewSet)
router.register(r'contactos-emergencia', ContactoEmergenciaViewSet)
router.register(r'sesiones', SesionViewSet)
router.register(r'reportes-sesion', ReporteSesionViewSet)
router.register(r'reportes-objetivos', ReporteObjetivoViewSet)
router.register(r'pagos', PagoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
