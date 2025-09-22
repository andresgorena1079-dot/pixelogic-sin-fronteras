# cursos/admin.py
from django.contrib import admin

# Añadimos CasoPrueba a la lista de importaciones
from .models import (
    CasoPrueba,
    Comentario,
    Curso,
    Herramienta,
    Juego,
    Leccion,
    Modulo,
    Perfil,
    Post,
)


# Clase especial para mejorar la vista de Herramientas y Juegos en el Admin
class RecursoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "autor", "estado", "fecha_creacion")
    list_filter = ("estado",)
    actions = ["aprobar_recursos"]

    def aprobar_recursos(self, request, queryset):
        queryset.update(estado="aprobado")

    aprobar_recursos.short_description = "Marcar seleccionados como Aprobados"


# Registramos los modelos que ya teníamos
admin.site.register(Curso)
admin.site.register(Modulo)
admin.site.register(Leccion)
admin.site.register(Post)
admin.site.register(Comentario)
admin.site.register(Perfil)

# Registramos los nuevos modelos usando la clase especial RecursoAdmin
admin.site.register(Herramienta, RecursoAdmin)
admin.site.register(Juego, RecursoAdmin)
admin.site.register(CasoPrueba)
