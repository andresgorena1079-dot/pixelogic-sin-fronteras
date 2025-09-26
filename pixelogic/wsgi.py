# pixelogic/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

# Apuntamos a nuestro archivo de settings unificado
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")

application = get_wsgi_application()

# --- ACTIVADO PARA LA CARGA DE DATOS EN RENDER ---
# IMPORTANTE: Comentar la línea 'exec(...)' después de la carga exitosa.
if os.environ.get("RENDER"):
    exec(open("startup.py").read())
