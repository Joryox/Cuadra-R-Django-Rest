import os, sys, django
sys.path.append('/home/popudo/Escritorio/Cuadra erre/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuadra_erre.settings')
django.setup()
from api.models import Sesion
from api.serializers import SesionSerializer, TutorReporteSesionSerializer, ReporteSesion
s = Sesion.objects.first()
if s:
    print("Sesion keys:", SesionSerializer(s).data.keys())
    print("Caballo:", SesionSerializer(s).data.get('caballo'))
r = ReporteSesion.objects.first()
if r:
    print("Reporte keys:", TutorReporteSesionSerializer(r).data.keys())
