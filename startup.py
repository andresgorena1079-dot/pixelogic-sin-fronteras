import os
import urllib.request

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")
django.setup()

from django.core.management import call_command

print("--- INICIANDO SCRIPT DE ARRANQUE EN RENDER ---")
DATA_URL = "LA_URL_DE_DESCARGA_DIRECTA_DE_TU_ARCHIVO_JSON"
FILENAME = "datos_produccion_final.json"

try:
    print(f"📥 Descargando datos desde la URL...")
    urllib.request.urlretrieve(DATA_URL, FILENAME)
    print(f"✅ Archivo '{FILENAME}' descargado exitosamente.")

    print("🧹 Limpiando la base de datos de producción...")
    call_command("flush", "--no-input")
    print("✅ Base de datos limpiada exitosamente.")

    print(f"📥 Cargando datos desde '{FILENAME}'...")
    call_command("loaddata", FILENAME)
    print("✅ Datos cargados exitosamente.")
except Exception as e:
    print(f"❌ Ocurrió un error durante la carga de datos: {e}")

print("--- SCRIPT DE ARRANQUE FINALIZADO ---")
