import os
from pathlib import Path

import dj_database_url
from decouple import config
from dotenv import load_dotenv

# === BASE Y SEGURIDAD ===
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

load_dotenv(os.path.join(BASE_DIR, ".env"))


# === CONFIGURACIÓN DE PRODUCCIÓN Y SEGURIDAD ===
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",
]
RENDER_EXTERNAL_HOSTNAME = config("RENDER_EXTERNAL_HOSTNAME", default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]

# ✅ MEJORA: Asegura que Django sepa que está detrás de un proxy seguro (como el de Render)
# Soluciona el error 'redirect_uri_mismatch' con Google.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "httpss")


# === APPS ===
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "cursos",
    # ✅ MEJORA: Apps para el almacenamiento de imágenes en la nube
    "cloudinary_storage",
    "cloudinary",
    "django_extensions",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

SITE_ID = 1


# === MIDDLEWARE ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    # ✅ MEJORA: Añadido para robustez, asegura que request.site siempre esté disponible
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
]

ROOT_URLCONF = "pixelogic.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pixelogic.wsgi.application"

# === BASE DE DATOS ===
DATABASES = {
    "default": dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

# === VALIDACIÓN DE CONTRASEÑAS ===
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# === INTERNACIONALIZACIÓN ===
LANGUAGE_CODE = "es-la"
TIME_ZONE = "America/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# === ARCHIVOS ESTÁTICOS Y MEDIA ===

# Configuración para archivos ESTÁTICOS (CSS, JS, imágenes de diseño) - Servidos por WhiteNoise
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# ✅ MEJORA: Configuración para archivos MEDIA (subidos por usuarios) - Servidos por Cloudinary
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

STORAGES = {
    # El almacenamiento por defecto para MEDIA es ahora Cloudinary
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    # El almacenamiento para ESTÁTICOS sigue siendo WhiteNoise
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# === ALLAUTH (AUTENTICACIÓN) ===
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/cuentas/login/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_LOGIN_ON_GET = True

# ✅ MEJORA: Le dice a allauth que genere las URLs de callback con https en producción
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"


# === CLOUDINARY ===
# Lee la URL de configuración desde tus variables de entorno (.env o en Render)
CLOUDINARY_URL = config("CLOUDINARY_URL", default=None)
