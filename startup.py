import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")
django.setup()

# ✅ Cargar datos completos
from django.core.management import call_command

if os.environ.get("RENDER"):
    print("📥 Cargando datos completos...")
    call_command("loaddata", "full_data.json")
    print("✅ Datos cargados")
