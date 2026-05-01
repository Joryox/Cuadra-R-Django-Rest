import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_config.settings')
django.setup()

from api.models import CatalogoEspecialidad

especialidades = [
    "Fisioterapia Equina",
    "Psicología Infantil",
    "Equinoterapia",
    "Médico Veterinario",
    "Asistente Terapéutico",
    "Recepción / Administración"
]

for esp in especialidades:
    CatalogoEspecialidad.objects.get_or_create(nombre=esp)

print("Especialidades creadas con éxito.")
