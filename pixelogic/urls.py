# EN pixelogic/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from cursos import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("allauth.urls")),
    path("", views.pagina_principal, name="pagina_principal"),
    path("cursos/", include("cursos.urls")),
    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
