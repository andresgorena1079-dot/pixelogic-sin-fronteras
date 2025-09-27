# startup.py (Versión para crear superusuario)
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")
django.setup()

from django.contrib.auth import get_user_model

print("--- INICIANDO SCRIPT DE ARRANQUE EN RENDER ---")

User = get_user_model()
username = "admin"
password = "admin123"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    print(f"Creando nuevo superusuario: {username}")
    try:
        User.objects.create_superuser(username, email, password)
        print("✅ Superusuario creado exitosamente.")
    except Exception as e:
        print(f"❌ Error al crear superusuario: {e}")
else:
    print(f"El superusuario '{username}' ya existe. No se realizaron cambios.")

print("--- SCRIPT DE ARRANQUE FINALIZADO ---")
