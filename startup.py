# startup.py (Versión final con descarga segura)
import os
import urllib.request

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")
django.setup()

from django.core.management import call_command

print("--- INICIANDO SCRIPT DE ARRANQUE EN RENDER (CON DESCARGA) ---")

# ==============================================================================
# IMPORTANTE: Pega aquí tu enlace de descarga directa del archivo de datos
# ==============================================================================
DATA_URL = "LA_URL_DE_DESCARGA_DIRECTA_DE_TU_ARCHIVO_JSON"
FILENAME = "datos_produccion_final.json"

try:
    # 1. Descargar el archivo de datos desde la URL
    print(f"📥 Descargando datos desde la URL...")
    urllib.request.urlretrieve(DATA_URL, FILENAME)
    print(f"✅ Archivo '{FILENAME}' descargado exitosamente.")

    # 2. Limpiar la base de datos de producción para una carga limpia
    print("🧹 Limpiando la base de datos de producción...")
    call_command("flush", "--no-input")
    print("✅ Base de datos limpiada exitosamente.")

    # 3. Cargar los datos desde el archivo descargado
    print(f"📥 Cargando datos desde '{FILENAME}'...")
    call_command("loaddata", FILENAME)
    print("✅ Datos cargados exitosamente.")

except Exception as e:
    print(f"❌ Ocurrió un error durante la carga de datos: {e}")

print("--- SCRIPT DE ARRANQUE FINALIZADO ---")
