from api.models import Usuario, Terapeuta, Paciente, Caballo

print(f"USUARIOS: {Usuario.objects.count()}")
print(f"TERAPEUTAS: {Terapeuta.objects.count()}")
print(f"PACIENTES: {Paciente.objects.count()}")
print(f"CABALLOS: {Caballo.objects.count()}")

# Verificar si hay discrepancias en las relaciones
for t in Terapeuta.objects.all():
    if not t.usuario:
        print(f"Terapeuta {t.id} sin usuario!")
    else:
        print(f"T: {t.usuario.nombre_completo} - Activo: {t.usuario.activo}")

for p in Paciente.objects.all():
    if not p.tutor:
        print(f"Paciente {p.nombre} sin tutor!")
    else:
        print(f"P: {p.nombre} - Tutor: {p.tutor.nombre_completo}")
