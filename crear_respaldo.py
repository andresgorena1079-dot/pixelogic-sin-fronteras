import os
import subprocess
import sys

print("Iniciando la creación del respaldo...")

output_filename = "datos_produccion_final.json"

command = [
    sys.executable,
    "manage.py",
    "dumpdata",
    "--natural-foreign",
    "--natural-primary",
    "-e",
    "contenttypes",
    "-e",
    "auth.permission",
]

try:
    my_env = os.environ.copy()
    my_env["PYTHONIOENCODING"] = "utf-8"

    # ✅ CAMBIO CLAVE: Capturamos la salida como bytes crudos, no como texto.
    result = subprocess.run(command, capture_output=True, check=True, env=my_env)

    # Decodificamos los bytes a texto UTF-8 manualmente.
    output_text = result.stdout.decode("utf-8")

    # Escribimos el texto decodificado al archivo.
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"✅ Respaldo '{output_filename}' creado exitosamente.")

except subprocess.CalledProcessError as e:
    print("❌ Error al ejecutar dumpdata.")
    print("--- SALIDA DE ERROR ---")
    # Decodificamos el error de forma segura, reemplazando caracteres problemáticos.
    error_text = e.stderr.decode("utf-8", errors="replace")
    print(error_text)
except Exception as e:
    print(f"❌ Ocurrió un error inesperado: {e}")
