import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_config.settings')
django.setup()

from api.models import Usuario, Rol
from django.contrib.auth.hashers import make_password

# Crear rol de admin si no existe
rol_admin, created = Rol.objects.get_or_create(nombre='Administrador')

# Check if admin already exists
admin_email = 'admin@cuadraerre.com'
admin_pass = '12345678'

user = Usuario.objects.filter(email=admin_email).first()

if not user:
    # Crear el usuario
    admin = Usuario.objects.create(
        rol=rol_admin,
        email=admin_email,
        password=make_password(admin_pass),
        nombre_completo='Admin Cuadra Erre',
        telefono='1234567890',
        activo=True
    )
    print(f"Administrador creado exitosamente: {admin.email}")
else:
    # Reset password of existing admin
    user.password = make_password(admin_pass)
    user.activo = True
    user.save()
    print(f"Contraseña de administrador actualizada a: {admin_pass}")
