# Despliegue de Cuadra Erre (Docker + Traefik)

Guía paso a paso para desplegar el stack completo (frontend, backend, base de
datos, Redis, archivos estáticos/media) en un VPS usando Docker Compose y
Traefik como punto de entrada único. Esta primera fase es **solo HTTP**
(sin dominio todavía); al final hay una sección para activar HTTPS cuando
tengas un dominio.

## 0. Prerrequisitos en el servidor

- Docker Engine + Docker Compose plugin instalados (`docker --version`,
  `docker compose version`).
- Puerto 80 libre (Traefik lo va a publicar).
- Acceso por SSH con permisos para correr Docker.
- Clonado el repo backend en el servidor:
  `git clone <url-backend> Cuadra-R-Django-Rest && cd Cuadra-R-Django-Rest`
- Clonado el repo frontend como hermano del backend (misma carpeta padre):
  ```
  algun-directorio/
    Backend/Cuadra-R-Django-Rest/   <- aquí vive docker-compose.yml
    Frontend/cuadra-r-frontend/
  ```
  El `docker-compose.yml` referencia el frontend con la ruta relativa
  `../../Frontend/cuadra-r-frontend`, así que la estructura de carpetas debe
  respetarse igual que en desarrollo.

## 1. Configurar variables de entorno

1. Copia la plantilla:
   ```bash
   cp .env.example .env
   ```
2. Edita `.env` y completa como mínimo:
   - `ENVIRONMENT=production`
   - `DJANGO_SECRET_KEY` — genera una nueva, NO reuses la de desarrollo:
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST=db`, `DB_PORT=5432`
     (`DB_HOST=db` porque así se llama el servicio de Postgres en compose).
   - `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — deben coincidir
     exactamente con `DB_NAME`/`DB_USER`/`DB_PASSWORD` (los usa el contenedor
     `db` para inicializarse).
   - `ALLOWED_HOSTS` — IP pública del servidor por ahora (ej. `203.0.113.10`),
     o el dominio cuando lo tengas.
   - `FRONTEND_URL` — mismo host, con esquema: `http://203.0.113.10`.
   - `CSRF_TRUSTED_ORIGINS` — igual que `FRONTEND_URL`: `http://203.0.113.10`.
   - `SECURE_SSL_REDIRECT=False`, `SESSION_COOKIE_SECURE=False`,
     `CSRF_COOKIE_SECURE=False` — **obligatorio mientras no haya HTTPS**, si
     se dejan en `True` el login no funcionará (las cookies "secure" no se
     envían por HTTP).
   - `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` — credenciales SMTP reales.
   - `REDIS_URL=redis://redis:6379/0`.
3. Verifica que NO se vaya a commitear este `.env` (ya está en
   `.gitignore`).

## 2. Construir las imágenes

```bash
docker compose build
```

Esto construye `backend` (Django + gunicorn) y `frontend` (Next.js
standalone). `traefik`, `db`, `redis` y `staticfiles` usan imágenes
oficiales, no requieren build.

## 3. Levantar el stack

```bash
docker compose up -d
```

Verifica que todo esté arriba y sano:

```bash
docker compose ps
```

Todos los servicios deben verse `running`/`healthy`. Revisa logs si alguno
falla:

```bash
docker compose logs -f backend
```

El contenedor `backend` al iniciar automáticamente:
1. Espera a que Postgres acepte conexiones.
2. Corre `python manage.py migrate --noinput`.
3. Corre `python manage.py collectstatic --noinput` (puebla el volumen que
   sirve el contenedor `staticfiles`).
4. Arranca gunicorn.

## 4. Crear el primer superusuario

```bash
docker compose exec backend python manage.py createsuperuser
```

(Si el proyecto ya tiene un comando de seed como `seed_test_data`, **no lo
corras en producción** — es solo para datos de prueba en local.)

## 5. Verificación funcional

```bash
curl -I http://<IP-DEL-SERVIDOR>/                          # 200, HTML de Next.js
curl -I http://<IP-DEL-SERVIDOR>/api/schema/swagger/        # 200, Swagger UI del backend
curl -I http://<IP-DEL-SERVIDOR>/static/admin/css/base.css  # 200, servido por el sidecar nginx
curl -I http://<IP-DEL-SERVIDOR>/admin/                     # 200/302, panel admin Django
```

Luego, desde el navegador:
- Entra a `http://<IP-DEL-SERVIDOR>/` y haz login real (flujo JWT completo).
- Sube una foto de un caballo desde el dashboard y confirma que se ve en
  `http://<IP-DEL-SERVIDOR>/media/caballos/...`.

## 6. Operaciones comunes

- Ver logs de un servicio: `docker compose logs -f <servicio>`
- Reiniciar solo el backend tras un cambio: `docker compose up -d --build backend`
- Backup de la base de datos:
  ```bash
  docker compose exec db pg_dump -U <DB_USER> <DB_NAME> > backup_$(date +%F).sql
  ```
- Aplicar nuevas migraciones tras un deploy: se hacen solas al reiniciar
  `backend` (paso 1 del entrypoint), o manualmente:
  ```bash
  docker compose exec backend python manage.py migrate
  ```

## 7. Activar HTTPS cuando tengas dominio (fase 2)

Cuando el dominio apunte (registro A) al servidor:

1. En `docker-compose.yml`, en el servicio `traefik`, descomenta el
   entrypoint `websecure` (puerto 443) y el `certificatesResolvers` con
   `letsencrypt` (ACME HTTP challenge), y añade tu email de contacto.
2. Cambia las reglas de los routers de `PathPrefix` a `Host(`tu-dominio.com`) && PathPrefix(...)` (o deja `PathPrefix` y añade el `Host` como
   condición adicional).
3. Añade el middleware de redirect HTTP→HTTPS al entrypoint `web`.
4. En `.env`: cambia `ALLOWED_HOSTS`, `FRONTEND_URL` y
   `CSRF_TRUSTED_ORIGINS` a `https://tu-dominio.com`, y pon
   `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`,
   `CSRF_COOKIE_SECURE=True`.
5. `docker compose up -d` para aplicar.
