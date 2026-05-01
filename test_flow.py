import httpx
import json

BASE_URL = "http://localhost:8000/api"

def test_full_flow():
    print("\n--- INICIANDO PRUEBA DE FLUJO GENERAL ---\n")

    # 1. Probar Login
    print("1. Probando Login de Administrador...")
    try:
        login_data = {"email": "admin@cuadraerre.com", "password": "12345678"}
        response = httpx.post(f"{BASE_URL}/login/", json=login_data)
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"   [OK] Login exitoso. Token generado.")
        else:
            print(f"   [ERROR] Login fallido: {response.text}")
            return
    except Exception as e:
        print(f"   [ERROR] Error de conexión: {e}")
        return

    # 2. Probar Catálogos (Leer de Postgres)
    print("\n2. Consultando Catálogo de Especialidades...")
    response = httpx.get(f"{BASE_URL}/especialidades/")
    if response.status_code == 200:
        count = len(response.json())
        print(f"   [OK] Se obtuvieron {count} especialidades desde PostgreSQL.")
    else:
        print(f"   [ERROR] Fallo al leer catálogos.")

    # 3. Registrar un Nuevo Paciente
    print("\n3. Registrando un Nuevo Paciente de Prueba...")
    paciente_data = {
        "paciente_nombre": "Juanito Prueba",
        "fecha_nacimiento": "2018-05-20",
        "peso_kg": 25.5,
        "tutor_nombre": "Tutor de Prueba",
        "tutor_email": "tutor.prueba@example.com",
        "tutor_password": "password123",
        "tutor_telefono": "5512345678",
        "es_mayor_de_edad": False,
        "direccion": "Calle de Prueba 123",
        "motivo_consulta": "Prueba de integración del sistema."
    }
    response = httpx.post(f"{BASE_URL}/pacientes/registrar/", json=paciente_data)
    if response.status_code == 201:
        paciente_id = response.json().get('id')
        print(f"   [OK] Paciente registrado con ID: {paciente_id}")
    else:
        print(f"   [ERROR] Error al registrar paciente: {response.text}")

    print("\n--- PRUEBAS FINALIZADAS CON ÉXITO ---")

if __name__ == "__main__":
    test_full_flow()
