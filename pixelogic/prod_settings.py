# pixelogic/prod_settings.py
from .settings import *  # Importa todo de settings.py

# Sobrescribe solo lo necesario para producción
DEBUG = False
ALLOWED_HOSTS = [".onrender.com"]

# Seguridad adicional para producción
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
