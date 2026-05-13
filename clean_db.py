import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_config.settings')
django.setup()

from api.models import Paciente, Caballo, Sesion, Terapeuta, ReporteSesion, BitacoraEquina
from django.contrib.auth import get_user_model

User = get_user_model()

print("Borrando Bitácoras Equinas...")
BitacoraEquina.objects.all().delete()

print("Borrando Reportes...")
ReporteSesion.objects.all().delete()

print("Borrando Sesiones...")
Sesion.objects.all().delete()

print("Borrando Pacientes (activos e inactivos)...")
try:
    Paciente.all_objects.all().delete()
except AttributeError:
    Paciente.objects.all().delete()

print("Borrando Caballos...")
Caballo.objects.all().delete()

print("Borrando Terapeutas de test...")
test_terapeutas = Terapeuta.objects.filter(usuario__nombre_completo__icontains='test')
for t in test_terapeutas:
    u = t.usuario
    t.delete()
    if u:
        u.delete()

print("Limpieza completada.")
