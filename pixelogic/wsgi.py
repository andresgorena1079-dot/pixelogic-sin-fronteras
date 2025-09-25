# pixelogic/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

# Apuntamos a nuestro archivo de settings unificado
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")

application = get_wsgi_application()

# La ejecución de startup.py ha sido eliminada.
