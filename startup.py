# startup.py
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")
django.setup()

from django.core.management import call_command

print("--- INICIANDO SCRIPT DE ARRANQUE EN RENDER ---")

try:
    # Paso 1: Limpiar la base de datos de producción para una carga limpia.
    print("🧹 Limpiando la base de datos de producción...")
    call_command("flush", "--no-input")
    print("✅ Base de datos limpiada exitosamente.")

    # Paso 2: Cargar los datos desde el archivo de respaldo.
    print("📥 Cargando datos desde 'datos_produccion_final.json'...")
    call_command("loaddata", "datos_produccion_final.json")
    print("✅ Datos cargados exitosamente.")

except Exception as e:
    print(f"❌ Ocurrió un error durante la carga de datos: {e}")

print("--- SCRIPT DE ARRANQUE FINALIZADO ---")
