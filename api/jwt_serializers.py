"""
jwt_serializers.py — Cuadra Erre Authentication Layer

Este archivo implementa el puente entre nuestro modelo 'Usuario' propio
(que NO hereda de AbstractUser) y la librería djangorestframework-simplejwt.

Por qué existe este archivo:
  SimpleJWT espera un modelo que herede de AbstractUser. Como Cuadra Erre
  usa un Usuario completamente personalizado, necesitamos un Backend de
  autenticación propio y un TokenSerializer que construya el JWT manualmente.
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from api.models import Usuario


# ==============================================================
# MAPA DE ROL → RUTA DE REDIRECCIÓN (usado por el Frontend)
# El Frontend Next.js lee 'redirect_to' del payload y navega.
# ==============================================================
ROL_REDIRECT_MAP = {
    'Administrador': '/dashboard',
    'Admin':         '/dashboard',
    'Terapeuta':     '/terapeuta/dashboard',
    'Tutor':         '/tutor/dashboard',
    'Paciente':      '/tutor/dashboard',  # Paciente adulto usa el portal tutor
}


class CuadraTokenObtainPairSerializer(serializers.Serializer):
    """
    Serializer de Login personalizado para el modelo Usuario de Cuadra Erre.

    Valida email + password contra nuestra tabla 'api_usuario',
    construye manualmente los tokens access/refresh de SimpleJWT,
    e inyecta claims personalizados (rol, nombre, redirect_to) en el payload.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # ── 1. Buscar usuario ──────────────────────────────────────────────────
        try:
            user = Usuario.objects.select_related('rol').get(email=email)
        except Usuario.DoesNotExist:
            # Mensaje genérico para evitar enumeración de cuentas
            raise serializers.ValidationError(
                {'detail': 'Credenciales inválidas.'},
                code='authentication'
            )

        # ── 2. Verificar que la cuenta esté activa ────────────────────────────
        if not user.activo:
            raise serializers.ValidationError(
                {'detail': 'Esta cuenta está desactivada. Contacta al administrador.'},
                code='authentication'
            )

        # ── 3. Verificar contraseña (bcrypt hash de Django) ───────────────────
        if not check_password(password, user.password):
            raise serializers.ValidationError(
                {'detail': 'Credenciales inválidas.'},
                code='authentication'
            )

        # ── 4. Construir tokens JWT manualmente ───────────────────────────────
        # Creamos el RefreshToken directamente (sin for_user) para evitar
        # la dependencia con AbstractUser y la tabla OutstandingToken.
        refresh = RefreshToken()
        refresh[api_settings.USER_ID_CLAIM] = str(user.id)

        # ── 5. Inyectar claims personalizados ─────────────────────────────────
        rol_nombre = user.rol.nombre
        redirect_to = ROL_REDIRECT_MAP.get(rol_nombre, '/dashboard')

        for token in (refresh, refresh.access_token):
            token['user_id']     = str(user.id)
            token['email']       = user.email
            token['nombre']      = user.nombre_completo
            token['rol']         = rol_nombre
            token['redirect_to'] = redirect_to

        return {
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id':          str(user.id),
                'nombre':      user.nombre_completo,
                'email':       user.email,
                'rol':         rol_nombre,
                'redirect_to': redirect_to,
            }
        }


class CuadraTokenRefreshSerializer(serializers.Serializer):
    """
    Serializer para renovar el access token usando el refresh token.
    Preserva los claims personalizados al rotar el token.
    """
    refresh = serializers.CharField()

    def validate(self, attrs):
        from rest_framework_simplejwt.tokens import RefreshToken as RT
        from rest_framework_simplejwt.exceptions import TokenError

        try:
            refresh = RT(attrs['refresh'])
        except TokenError as e:
            raise serializers.ValidationError({'detail': str(e)})

        # El nuevo access token hereda los claims del refresh
        access = refresh.access_token

        return {
            'access':  str(access),
            'refresh': str(refresh),
        }
