"""
Cuadra Erre — Production Settings
Configuración para producción / despliegue.
Activa con: ENVIRONMENT=production
"""

from .base import *  # noqa: F401,F403

DEBUG = False

# En producción, DEBES definir tus dominios reales
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Base de datos: PostgreSQL siempre en producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# CORS: solo el dominio real del frontend
FRONTEND_URL = os.getenv('FRONTEND_URL', '')
CORS_ALLOWED_ORIGINS = [url.strip() for url in FRONTEND_URL.split(',') if url.strip()]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
]

# CSRF: orígenes de confianza detrás de Traefik (debe incluir el esquema,
# ej. "http://203.0.113.10" o "https://tu-dominio.com")
CSRF_TRUSTED_ORIGINS = [
    url.strip() for url in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if url.strip()
]

# Seguridad HTTPS
# NOTA: mientras no haya dominio/HTTPS, estas 3 deben ir en False vía .env,
# si no el login se rompe (las cookies "secure" no se mandan por HTTP plano).
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True').lower() == 'true'
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Solo JSON en producción (no Browsable API)
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [  # noqa: F405
    'rest_framework.renderers.JSONRenderer',
]
