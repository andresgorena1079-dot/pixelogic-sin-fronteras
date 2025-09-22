"""
WSGI config for pixelogic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# pixelogic/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

# Cambiamos 'pixelogic.settings' por 'pixelogic.prod_settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")

application = get_wsgi_application()
