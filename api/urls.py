from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import *

router = DefaultRouter(trailing_slash=False)

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
router.register(r'bitacora-seguridad', BitacoraSeguridadViewSet)


urlpatterns = [
    path('login', login_view, name='api-login'),
    path('terapeutas/registrar', registrar_terapeuta, name='api-registrar-terapeuta'),
    path('terapeutas/registrar/<uuid:pk>', registrar_terapeuta, name='api-actualizar-terapeuta'),
    path('pacientes/registrar', registrar_paciente, name='api-registrar-paciente'),
    path('usuarios/<uuid:usuario_id>/reset-password', resetear_password, name='api-reset-password'),
    path('usuarios/<uuid:usuario_id>/profile', update_profile, name='api-update-profile'),
    path('usuarios/<uuid:usuario_id>/change-password', change_password, name='api-change-password'),
    path('dashboard-stats', dashboard_stats, name='api-dashboard-stats'),

    path('', include(router.urls)),
]

