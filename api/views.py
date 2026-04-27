from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import (
    Rol, Usuario, CatalogoEspecialidad, CatalogoDiagnostico,
    CatalogoObjetivo, CatalogoEstadoCaballo, CatalogoEventoEquino,
    CatalogoEstadoSesion, CatalogoEstadoPago, CatalogoParentesco,
    Terapeuta, Caballo, BitacoraEquina, Paciente, PacienteDiagnostico,
    ContactoEmergencia, Sesion, ReporteSesion, ReporteObjetivo, Pago
)
from api.serializers import *
import httpx

# --- Catálogos ---
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class CatalogoEspecialidadViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEspecialidad.objects.all()
    serializer_class = CatalogoEspecialidadSerializer

class CatalogoDiagnosticoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoDiagnostico.objects.all()
    serializer_class = CatalogoDiagnosticoSerializer

class CatalogoObjetivoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoObjetivo.objects.all()
    serializer_class = CatalogoObjetivoSerializer

class CatalogoEstadoCaballoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEstadoCaballo.objects.all()
    serializer_class = CatalogoEstadoCaballoSerializer

class CatalogoEventoEquinoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEventoEquino.objects.all()
    serializer_class = CatalogoEventoEquinoSerializer

class CatalogoEstadoSesionViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEstadoSesion.objects.all()
    serializer_class = CatalogoEstadoSesionSerializer

class CatalogoEstadoPagoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEstadoPago.objects.all()
    serializer_class = CatalogoEstadoPagoSerializer

class CatalogoParentescoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoParentesco.objects.all()
    serializer_class = CatalogoParentescoSerializer

# --- Modelos Core ---
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class TerapeutaViewSet(viewsets.ModelViewSet):
    queryset = Terapeuta.objects.all()
    serializer_class = TerapeutaSerializer

class CaballoViewSet(viewsets.ModelViewSet):
    queryset = Caballo.objects.all()
    serializer_class = CaballoSerializer

class BitacoraEquinaViewSet(viewsets.ModelViewSet):
    queryset = BitacoraEquina.objects.all()
    serializer_class = BitacoraEquinaSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class PacienteDiagnosticoViewSet(viewsets.ModelViewSet):
    queryset = PacienteDiagnostico.objects.all()
    serializer_class = PacienteDiagnosticoSerializer

class ContactoEmergenciaViewSet(viewsets.ModelViewSet):
    queryset = ContactoEmergencia.objects.all()
    serializer_class = ContactoEmergenciaSerializer

class SesionViewSet(viewsets.ModelViewSet):
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer

    def create(self, request, *args, **kwargs):
        # REGLA 2: Bienestar Animal
        caballo_id = request.data.get('caballo')
        paciente_id = request.data.get('paciente')
        
        try:
            caballo = Caballo.objects.get(id=caballo_id)
            paciente = Paciente.objects.get(id=paciente_id)
            
            # a) El estado de salud debe ser Activo
            if caballo.estado_salud.nombre.lower() != 'activo':
                return Response({"error": "El caballo no está en estado Activo."}, status=status.HTTP_400_BAD_REQUEST)
                
            # b) El peso del paciente NO debe superar el peso soportado por el caballo
            if paciente.peso_kg > caballo.peso_max_soporta:
                return Response({"error": "El paciente supera el peso máximo que soporta este caballo."}, status=status.HTTP_400_BAD_REQUEST)
                
        except (Caballo.DoesNotExist, Paciente.DoesNotExist):
            return Response({"error": "Caballo o Paciente no encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class ReporteSesionViewSet(viewsets.ModelViewSet):
    queryset = ReporteSesion.objects.all()
    serializer_class = ReporteSesionSerializer

    def perform_create(self, serializer):
        # REGLA 3: Webhook a n8n
        instance = serializer.save()
        try:
            payload = {
                "nombre_paciente": instance.sesion.paciente.nombre,
                "telefono_tutor": instance.sesion.paciente.tutor.telefono,
                "recomendacion_casa": instance.recomendacion_casa,
                "objetivos_trabajados": "N/A" # Pendiente
            }
            # requests.post('URL_DE_N8N', json=payload, timeout=5)
            print("Webhook disparado a n8n:", payload)
        except Exception as e:
            print("Error disparando webhook:", e)

class ReporteObjetivoViewSet(viewsets.ModelViewSet):
    queryset = ReporteObjetivo.objects.all()
    serializer_class = ReporteObjetivoSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
