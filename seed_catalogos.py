import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_config.settings')
django.setup()

from api.models import (
    CatalogoEstadoSesion, CatalogoEstadoPago,
    CatalogoObjetivo, CatalogoDiagnostico,
    CatalogoEstadoCaballo, CatalogoParentesco
)

def seed():
    # Estados de Sesión
    estados_sesion = ['Programada', 'En Curso', 'Finalizada', 'Cancelada']
    for nombre in estados_sesion:
        CatalogoEstadoSesion.objects.get_or_create(nombre=nombre)
    print(f"[OK] {len(estados_sesion)} estados de sesion creados")
    estados_pago = ['Pendiente', 'Pagado', 'Vencido', 'Condonado']
    for nombre in estados_pago:
        CatalogoEstadoPago.objects.get_or_create(nombre=nombre)
    print(f"[OK] {len(estados_pago)} estados de pago creados")
    objetivos = [
        'Mejorar equilibrio',
        'Control postural',
        'Estimulacion sensorial',
        'Coordinacion motora',
        'Relajacion y manejo de ansiedad',
        'Socializacion',
        'Comunicacion verbal y no verbal',
        'Fortalecimiento muscular',
        'Independencia funcional',
        'Regulacion emocional',
    ]
    for nombre in objetivos:
        CatalogoObjetivo.objects.get_or_create(nombre=nombre)
    print(f"[OK] {len(objetivos)} objetivos terapeuticos creados")
    diagnosticos = [
        'Paralisis Cerebral Infantil (PCI)',
        'Trastorno del Espectro Autista (TEA)',
        'Sindrome de Down',
        'TDAH',
        'Discapacidad intelectual',
        'Trastorno del lenguaje',
        'Retraso psicomotor',
        'Distrofia muscular',
        'Lesion medular',
        'Trastorno de ansiedad',
    ]
    for nombre in diagnosticos:
        CatalogoDiagnostico.objects.get_or_create(nombre=nombre)
    print(f"[OK] {len(diagnosticos)} diagnosticos creados")
    estados_caballo = ['Activo', 'Reposo', 'Atencion Medica', 'Retirado']
    for nombre in estados_caballo:
        CatalogoEstadoCaballo.objects.get_or_create(nombre=nombre)
    print(f"[OK] {len(estados_caballo)} estados de caballo creados")
    parentescos = ['Madre', 'Padre', 'Abuelo/a', 'Tutor Legal', 'Hermano/a', 'Tio/a', 'Otro']
    for nombre in parentescos:
        CatalogoParentesco.objects.get_or_create(nombre=nombre)
    print(f"[OK] {len(parentescos)} parentescos creados")
    print("Todos los catalogos sembrados correctamente.")

if __name__ == '__main__':
    seed()
