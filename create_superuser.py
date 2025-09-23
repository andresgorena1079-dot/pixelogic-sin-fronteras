import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@pixelogic.com", "admin123")
    print("✅ Superusuario 'admin' creado")
else:
    print("ℹ️ El usuario 'admin' ya existe")
