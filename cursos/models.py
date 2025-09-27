# cursos/models.py

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    logo = models.ImageField(upload_to="logos_cursos/", blank=True, null=True)

    def __str__(self):
        return self.titulo


class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo


class Leccion(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.CharField(
        max_length=255, blank=True, help_text="Un resumen corto de la lección."
    )
    contenido_html = models.TextField()
    codigo_ejercicio = models.TextField(
        blank=True, help_text="Código inicial para la zona de práctica de esta lección."
    )
    instrucciones_ejercicio = models.TextField(
        blank=True,
        help_text="El HTML con las instrucciones del ejercicio para la zona de práctica.",
    )
    puntos_xp = models.IntegerField(
        default=10, help_text="Puntos de experiencia ganados al completar la lección."
    )
    orden = models.IntegerField(default=0)
    usuarios_completado = models.ManyToManyField(
        User, related_name="lecciones_completadas", blank=True
    )

    def __str__(self):
        return self.titulo


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    total_xp = models.IntegerField(default=0)

    def __str__(self):
        return self.usuario.username

    @receiver(post_save, sender=User)
    def crear_o_actualizar_perfil_usuario(sender, instance, created, **kwargs):
        if hasattr(instance, "perfil"):
            instance.perfil.save()
        else:
            Perfil.objects.create(usuario=instance)


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    me_gusta = models.ManyToManyField(
        User, related_name="posts_con_me_gusta", blank=True
    )
    imagen = models.ImageField(upload_to="post_imagenes/", blank=True, null=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    me_gusta = models.ManyToManyField(
        User, related_name="comentarios_con_me_gusta", blank=True
    )

    def __str__(self):
        return f'Comentario de {self.autor.username} en "{self.post.titulo}"'


class Herramienta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    enlace = models.URLField(
        blank=True, null=True, help_text="Enlace opcional si subes un archivo."
    )
    archivo = models.FileField(
        upload_to="herramientas_archivos/",
        blank=True,
        null=True,
        help_text="Sube el instalador o archivo .zip aquí.",
    )
    imagen = models.ImageField(upload_to="herramientas/", blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default="pendiente")
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    enlace = models.URLField(
        blank=True, null=True, help_text="Enlace opcional si subes un archivo."
    )
    archivo = models.FileField(
        upload_to="juegos_archivos/",
        blank=True,
        null=True,
        help_text="Sube el juego o archivo .zip aquí.",
    )
    imagen = models.ImageField(upload_to="juegos/", blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default="pendiente")
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class CasoPrueba(models.Model):
    leccion = models.ForeignKey(
        Leccion, on_delete=models.CASCADE, related_name="casos_prueba"
    )
    expresion_a_evaluar = models.TextField(
        help_text="El código a ejecutar o una descripción. Ej: mi_funcion(2, 3)"
    )
    resultado_esperado = models.TextField(
        help_text="La salida de texto exacta que se espera. Ej: 5"
    )

    def __str__(self):
        return f"Caso de prueba para '{self.leccion.titulo}'"
