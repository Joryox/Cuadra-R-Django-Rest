import urllib.request
import json

try:
    with urllib.request.urlopen('http://127.0.0.1:8000/api/pacientes/') as response:
        data = response.read().decode()
        print("STATUS: OK")
        print(data)
except Exception as e:
    print(f"ERROR: {e}")
