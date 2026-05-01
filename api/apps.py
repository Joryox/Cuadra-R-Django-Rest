from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        import os
        import sys
        # Evitar que se ejecute dos veces con el reloader de Django
        # Y evitar que se ejecute si ya estamos corriendo el comando de setup
        if (os.environ.get('RUN_MAIN') == 'true' or 'runserver' not in sys.argv) and 'setup_db' not in sys.argv:
            from django.core.management import call_command
            try:
                print("Checking database setup...")
                call_command('setup_db')
            except Exception as e:
                print(f"Error en auto-setup: {e}")
