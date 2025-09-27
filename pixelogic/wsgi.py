# pixelogic/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")
application = get_wsgi_application()

# --- ACTIVADO PARA LA CARGA DE DATOS EN RENDER ---
# IMPORTANTE: Comentar esta línea después de la carga exitosa.
if os.environ.get("RENDER"):
    exec(open("startup.py").read())
