# startup.py (Versión final para ACTUALIZAR datos)
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")
django.setup()

from django.core.management import call_command

print("--- INICIANDO SCRIPT DE ARRANQUE EN RENDER (MODO ACTUALIZACIÓN) ---")

try:
    # Ya no ejecutamos 'flush'. Cargamos los datos directamente.
    print("📥 Cargando datos desde 'datos_produccion_final.json'...")
    call_command("loaddata", "datos_produccion_final.json")
    print("✅ Datos cargados y actualizados exitosamente.")

except Exception as e:
    print(f"❌ Ocurrió un error durante la carga de datos: {e}")

print("--- SCRIPT DE ARRANQUE FINALIZADO ---")
