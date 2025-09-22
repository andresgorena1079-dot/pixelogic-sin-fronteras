from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from cursos import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("allauth.urls")),
    # Ruta para la página principal (homepage)
    path("", views.pagina_principal, name="pagina_principal"),
    # Delega todo lo que empiece con /cursos/ a la app 'cursos'
    path("cursos/", include("cursos.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
