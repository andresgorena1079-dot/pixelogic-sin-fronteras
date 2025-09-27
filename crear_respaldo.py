# crear_respaldo.py (Versión final que EXCLUYE secretos Y perfiles)
import os
import sys

import django

print("Iniciando la creación del respaldo limpio (sin secretos ni perfiles)...")

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")
    django.setup()
    from django.core.management import call_command

    output_filename = "datos_produccion_final.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        original_stdout = sys.stdout
        sys.stdout = f

        call_command(
            "dumpdata",
            "--natural-foreign",
            "--natural-primary",
            "-e",
            "contenttypes",
            "-e",
            "auth.permission",
            "--exclude",
            "socialaccount.socialapp",  # <-- EXCLUYE LAS CLAVES DE GOOGLE
            "-e",
            "cursos.perfil",  # <-- AÑADE ESTA LÍNEA PARA EXCLUIR LOS PERFILES
        )

    sys.stdout = original_stdout
    print(f"✅ Respaldo limpio '{output_filename}' creado exitosamente.")

except Exception as e:
    if "original_stdout" in locals():
        sys.stdout = original_stdout
    print(f"❌ Ocurrió un error inesperado: {e}")
