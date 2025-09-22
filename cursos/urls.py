from django.urls import path

from . import views

# Definimos el namespace para evitar conflictos de nombres
app_name = "cursos"

urlpatterns = [
    # --- Rutas de Cursos (Existentes) ---
    path("perfil/<str:username>/", views.vista_perfil, name="vista_perfil"),
    path("", views.lista_cursos, name="lista_cursos"),
    path("<int:curso_id>/", views.detalle_curso, name="detalle_curso"),
    path("api/execute-code/", views.execute_code, name="execute_code"),
    path("modulo/<int:modulo_id>/", views.detalle_modulo, name="detalle_modulo"),
    path("leccion/<int:leccion_id>/", views.detalle_leccion, name="detalle_leccion"),
    path(
        "leccion/<int:leccion_id>/completar/",
        views.completar_leccion,
        name="completar_leccion",
    ),
    # --- NUEVA RUTA PARA LA ZONA DE PRÁCTICA ---
    path(
        "leccion/<int:leccion_id>/practica/", views.zona_practica, name="zona_practica"
    ),
    path("api/execute-code/", views.execute_code, name="execute_code"),
    path("api/validar-codigo/", views.validar_codigo, name="validar_codigo"),
    # --- Rutas de Comunidad (Existentes) ---
    path("comunidad/", views.lista_posts, name="lista_posts"),
    path("comunidad/post/<int:post_id>/", views.detalle_post, name="detalle_post"),
    path("comunidad/crear/", views.crear_post, name="crear_post"),
    path(
        "comunidad/eliminar/<int:post_id>/", views.eliminar_post, name="eliminar_post"
    ),
    path(
        "comunidad/me_gusta/<int:post_id>/", views.me_gusta_post, name="me_gusta_post"
    ),
    path(
        "comunidad/me_gusta_comentario/<int:comentario_id>/",
        views.me_gusta_comentario,
        name="me_gusta_comentario",
    ),
    # --- Rutas de Herramientas y Juegos (Existentes) ---
    path("herramientas/", views.lista_herramientas, name="lista_herramientas"),
    path("herramientas/subir/", views.subir_herramienta, name="subir_herramienta"),
    path("juegos/", views.lista_juegos, name="lista_juegos"),
    path("juegos/subir/", views.subir_juego, name="subir_juego"),
    path(
        "herramientas/editar/<int:herramienta_id>/",
        views.editar_herramienta,
        name="editar_herramienta",
    ),
    path("juegos/editar/<int:juego_id>/", views.editar_juego, name="editar_juego"),
    path(
        "herramientas/eliminar/<int:herramienta_id>/",
        views.eliminar_herramienta,
        name="eliminar_herramienta",
    ),
    path(
        "juegos/eliminar/<int:juego_id>/", views.eliminar_juego, name="eliminar_juego"
    ),
    path(
        "herramienta/<int:herramienta_id>/track/",
        views.track_click_herramienta,
        name="track_click_herramienta",
    ),
    path(
        "juego/<int:juego_id>/track/", views.track_click_juego, name="track_click_juego"
    ),
]
