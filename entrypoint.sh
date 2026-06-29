#!/bin/sh
set -e

echo "Esperando a Postgres en ${DB_HOST:-db}:${DB_PORT:-5432}..."
python -c "
import os, socket, time
host = os.getenv('DB_HOST', 'db')
port = int(os.getenv('DB_PORT', '5432'))
for _ in range(60):
    try:
        socket.create_connection((host, port), timeout=2).close()
        break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit('Postgres no respondio a tiempo')
"
echo "Postgres listo."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn core_config.wsgi:application --bind 0.0.0.0:8000 --workers 3
