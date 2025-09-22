# pixelogic/prod_settings.py
import os

import dj_database_url

from .settings import ALLOWED_HOSTS, DATABASES, MIDDLEWARE

DEBUG = False

# Configuración de la URL de Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Configuración de la base de datos de Render
DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# Configuración de WhiteNoise para archivos estáticos
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
