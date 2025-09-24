"""
WSGI config for pixelogic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# pixelogic/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

# CAMBIA ESTO:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.prod_settings")

application = get_wsgi_application()

# Forzar creación de superusuario al arrancar
import os

if os.environ.get("RENDER"):
    exec(open("startup.py").read())
