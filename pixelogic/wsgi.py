# pixelogic/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

# Cambiamos 'pixelogic.settings' por 'pixelogic.prod_settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.prod_settings")

application = get_wsgi_application()
