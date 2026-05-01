import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_config.settings')
django.setup()

from api.models import Caballo, CatalogoEstadoCaballo

def seed_caballos():
    estado_activo, _ = CatalogoEstadoCaballo.objects.get_or_create(nombre='Activo')
    estado_reposo, _ = CatalogoEstadoCaballo.objects.get_or_create(nombre='Reposo')
    
    caballos_data = [
        {
            "nombre": "Relámpago",
            "raza": "Pura Sangre",
            "peso_max_soporta": 85.00,
            "sesiones_semanales_max": 10,
            "activo": True,
            "disponible": True,
            "estado_salud": estado_activo
        },
        {
            "nombre": "Luna",
            "raza": "Árabe",
            "peso_max_soporta": 75.00,
            "sesiones_semanales_max": 8,
            "activo": True,
            "disponible": True,
            "estado_salud": estado_activo
        },
        {
            "nombre": "Trueno",
            "raza": "Cuarto de Milla",
            "peso_max_soporta": 95.00,
            "sesiones_semanales_max": 12,
            "activo": False,
            "disponible": False,
            "estado_salud": estado_reposo,
            "motivo_inactividad": "Lesión leve en pata derecha"
        }
    ]
    
    for data in caballos_data:
        Caballo.objects.get_or_create(
            nombre=data["nombre"],
            defaults={
                "raza": data["raza"],
                "peso_max_soporta": data["peso_max_soporta"],
                "sesiones_semanales_max": data["sesiones_semanales_max"],
                "activo": data["activo"],
                "disponible": data["disponible"],
                "estado_salud": data["estado_salud"],
                "motivo_inactividad": data.get("motivo_inactividad", "")
            }
        )
    print(f"[OK] {len(caballos_data)} caballos creados en la base de datos.")

if __name__ == "__main__":
    seed_caballos()
