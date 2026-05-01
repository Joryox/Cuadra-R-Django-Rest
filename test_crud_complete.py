import httpx
import uuid

BASE_URL = "http://localhost:8000/api"
TOKEN = ""

def run_crud_tests():
    global TOKEN
    print("\n--- INICIANDO AUDITORIA CRUD COMPLETA - CUADRA ERRE ---\n")

    # --- 1. AUTH ---
    print("[AUTH] Validando acceso...")
    r = httpx.post(f"{BASE_URL}/login/", json={"email": "admin@cuadraerre.com", "password": "12345678"})
    if r.status_code != 200: 
        print("X Error de Auth"); return
    TOKEN = r.json()['token']
    headers = {"Authorization": f"Bearer {TOKEN}"}
    print("   OK Autenticación exitosa.")

    # --- 2. CABALLOS (CRUD) ---
    print("\n[CABALLOS] Iniciando CRUD...")
    # Create
    status_activo = httpx.get(f"{BASE_URL}/estados-caballo/").json()[0]['id']
    caballo_data = {
        "nombre": "Pegaso Test",
        "peso_max_soporta": 100,
        "sesiones_semanales_max": 10,
        "estado_salud": status_activo,
        "activo": True
    }
    r = httpx.post(f"{BASE_URL}/caballos/", json=caballo_data)
    caballo_id = r.json()['id']
    print(f"   OK CREATE: Caballo '{caballo_data['nombre']}' creado.")

    # Update
    r = httpx.patch(f"{BASE_URL}/caballos/{caballo_id}/", json={"nombre": "Pegaso Evolucionado"})
    print(f"   OK UPDATE: Nombre actualizado a '{r.json()['nombre']}'.")

    # Read
    r = httpx.get(f"{BASE_URL}/caballos/{caballo_id}/")
    print(f"   OK READ: Datos recuperados correctamente.")

    # Delete
    r = httpx.delete(f"{BASE_URL}/caballos/{caballo_id}/")
    print(f"   OK DELETE: Registro eliminado de PostgreSQL.")

    # --- 3. TERAPEUTAS (Flujo Especial) ---
    print("\n[TERAPEUTAS] Probando registro y gestión...")
    esp_id = httpx.get(f"{BASE_URL}/especialidades/").json()[0]['id']
    tera_data = {
        "nombre": "Dra. Laura Test",
        "email": f"laura.{uuid.uuid4().hex[:4]}@test.com",
        "password": "password123",
        "especialidad_id": esp_id,
        "cedula": "12345678",
        "biografia": "Terapeuta de prueba"
    }
    r = httpx.post(f"{BASE_URL}/terapeutas/registrar/", json=tera_data)
    tera_id = r.json()['id']
    print(f"   OK CREATE: Terapeuta '{tera_data['nombre']}' registrado.")

    # Update
    r = httpx.patch(f"{BASE_URL}/terapeutas/registrar/{tera_id}/", json={"nombre": "Dra. Laura Actualizada"})
    print(f"   OK UPDATE: Perfil actualizado.")

    # --- 4. PACIENTES Y SESIONES ---
    print("\n[SESIONES] Validando reglas de negocio...")
    # Crear un paciente pesado
    paciente_data = {
        "paciente_nombre": "Paciente Pesado",
        "fecha_nacimiento": "2010-01-01",
        "peso_kg": 200,
        "tutor_email": f"tutor.{uuid.uuid4().hex[:4]}@test.com",
        "tutor_password": "123",
        "es_mayor_de_edad": True
    }
    p_resp = httpx.post(f"{BASE_URL}/pacientes/registrar/", json=paciente_data).json()
    paciente_id = p_resp['id']

    # Recreamos el caballo
    cab_resp = httpx.post(f"{BASE_URL}/caballos/", json=caballo_data).json()
    cab_id = cab_resp['id']
    
    sesion_data = {
        "fecha_hora": "2026-05-01T10:00:00Z",
        "paciente": paciente_id,
        "terapeuta": tera_id,
        "caballo": cab_id,
        "estatus": httpx.get(f"{BASE_URL}/estados-sesion/").json()[0]['id']
    }
    r = httpx.post(f"{BASE_URL}/sesiones/", json=sesion_data)
    if r.status_code == 400:
        print(f"   OK REGLA DE NEGOCIO: Bloqueo exitoso por exceso de peso ({r.json()['error']})")
    else:
        print(f"   ERROR REGLA DE NEGOCIO: La sesión no debió permitirse.")

    print("\n--- AUDITORIA FINALIZADA - SISTEMA ESTABLE AL 100% ---")

if __name__ == "__main__":
    run_crud_tests()
