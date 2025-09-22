import ast
import io
import json
import os
import re
import subprocess
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import HerramientaForm, JuegoForm
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


def pagina_principal(request):
    cursos_destacados = Curso.objects.annotate(
        total_lecciones=Count("modulo__leccion", distinct=True)
    ).order_by("id")[:3]
    if request.user.is_authenticated:
        cursos_destacados = cursos_destacados.annotate(
            lecciones_completadas=Count(
                "modulo__leccion",
                filter=Q(modulo__leccion__usuarios_completado=request.user),
                distinct=True,
            )
        )
    for curso in cursos_destacados:
        if hasattr(curso, "lecciones_completadas") and curso.total_lecciones > 0:
            curso.progreso_porcentaje = int(
                (curso.lecciones_completadas / curso.total_lecciones) * 100
            )
        else:
            curso.progreso_porcentaje = 0
    ultimos_posts = Post.objects.order_by("-fecha_publicacion")[:3]
    contexto = {
        "cursos_destacados": cursos_destacados,
        "ultimos_posts": ultimos_posts,
    }
    return render(request, "index.html", contexto)


def lista_cursos(request):
    cursos = Curso.objects.annotate(
        total_lecciones=Count("modulo__leccion", distinct=True)
    )
    if request.user.is_authenticated:
        cursos = cursos.annotate(
            lecciones_completadas=Count(
                "modulo__leccion",
                filter=Q(modulo__leccion__usuarios_completado=request.user),
                distinct=True,
            )
        )
    for curso in cursos:
        if hasattr(curso, "lecciones_completadas") and curso.total_lecciones > 0:
            curso.progreso_porcentaje = int(
                (curso.lecciones_completadas / curso.total_lecciones) * 100
            )
        else:
            curso.progreso_porcentaje = 0
    contexto = {"cursos": cursos}
    return render(request, "cursos/lista_cursos.html", contexto)


def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    modulos = (
        Modulo.objects.filter(curso=curso)
        .order_by("id")
        .annotate(total_lecciones=Count("leccion"))
    )
    if request.user.is_authenticated:
        modulos = modulos.annotate(
            lecciones_completadas=Count(
                "leccion", filter=Q(leccion__usuarios_completado=request.user)
            )
        )
    for modulo in modulos:
        if hasattr(modulo, "lecciones_completadas") and modulo.total_lecciones > 0:
            modulo.progreso_porcentaje = int(
                (modulo.lecciones_completadas / modulo.total_lecciones) * 100
            )
        else:
            modulo.progreso_porcentaje = 0
    contexto = {"curso": curso, "modulos": modulos}
    return render(request, "cursos/detalle_curso.html", contexto)


def detalle_modulo(request, modulo_id):
    modulo = get_object_or_404(Modulo, pk=modulo_id)
    lecciones = Leccion.objects.filter(modulo=modulo).order_by("orden")
    if not request.user.is_authenticated:
        for i, leccion in enumerate(lecciones):
            if i > 0:
                leccion.bloqueada = True
    lecciones_completadas_ids = set()
    if request.user.is_authenticated:
        lecciones_completadas_ids = set(
            Leccion.objects.filter(
                usuarios_completado=request.user, modulo=modulo
            ).values_list("id", flat=True)
        )
    contexto = {
        "modulo": modulo,
        "lecciones": lecciones,
        "lecciones_completadas_ids": lecciones_completadas_ids,
    }
    return render(request, "cursos/detalle_modulo.html", contexto)


def detalle_leccion(request, leccion_id):
    leccion = get_object_or_404(Leccion, pk=leccion_id)
    completada = False
    if request.user.is_authenticated:
        completada = leccion.usuarios_completado.filter(pk=request.user.pk).exists()
    leccion_anterior = (
        Leccion.objects.filter(modulo=leccion.modulo, orden__lt=leccion.orden)
        .order_by("-orden")
        .first()
    )
    leccion_siguiente = (
        Leccion.objects.filter(modulo=leccion.modulo, orden__gt=leccion.orden)
        .order_by("orden")
        .first()
    )
    contexto = {
        "leccion": leccion,
        "completada": completada,
        "leccion_anterior": leccion_anterior,
        "leccion_siguiente": leccion_siguiente,
    }
    return render(request, "cursos/detalle_leccion.html", contexto)


@login_required
def completar_leccion(request, leccion_id):
    leccion = get_object_or_404(Leccion, pk=leccion_id)
    ya_completada = leccion.usuarios_completado.filter(pk=request.user.pk).exists()
    if not ya_completada:
        leccion.usuarios_completado.add(request.user)
        perfil = request.user.perfil
        perfil.total_xp += leccion.puntos_xp
        perfil.save()
        messages.success(
            request, f"¡Lección completada! Has ganado {leccion.puntos_xp} XP."
        )
    leccion_siguiente = (
        Leccion.objects.filter(modulo=leccion.modulo, orden__gt=leccion.orden)
        .order_by("orden")
        .first()
    )
    if leccion_siguiente:
        return redirect("cursos:detalle_leccion", leccion_id=leccion_siguiente.id)
    else:
        return redirect("cursos:detalle_modulo", modulo_id=leccion.modulo.id)


@login_required
def lista_posts(request):
    posts = Post.objects.annotate(me_gusta_count=Count("me_gusta")).order_by(
        "-fecha_publicacion"
    )
    contexto = {"posts": posts}
    return render(request, "comunidad/lista_posts.html", contexto)


@login_required
def detalle_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comentarios = Comentario.objects.filter(post=post).order_by("fecha_publicacion")
    if request.method == "POST":
        if request.user.is_authenticated:
            contenido = request.POST.get("contenido")
            if contenido:
                Comentario.objects.create(
                    post=post, autor=request.user, contenido=contenido
                )
            return redirect("cursos:detalle_post", post_id=post.id)
    contexto = {"post": post, "comentarios": comentarios}
    return render(request, "comunidad/detalle_post.html", contexto)


@login_required
def crear_post(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        contenido = request.POST.get("contenido")
        if titulo and contenido:
            Post.objects.create(titulo=titulo, contenido=contenido, autor=request.user)
            return redirect("cursos:lista_posts")
    return render(request, "comunidad/crear_post.html")


@login_required
def eliminar_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.autor or request.user.is_superuser:
        post.delete()
    return redirect("cursos:lista_posts")


@login_required
def me_gusta_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.me_gusta.all():
        post.me_gusta.remove(request.user)
    else:
        post.me_gusta.add(request.user)
    return redirect("cursos:detalle_post", post_id=post.id)


@login_required
def me_gusta_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    if request.user in comentario.me_gusta.all():
        comentario.me_gusta.remove(request.user)
    else:
        comentario.me_gusta.add(request.user)
    return redirect("cursos:detalle_post", post_id=comentario.post.id)


def lista_herramientas(request):
    herramientas = Herramienta.objects.filter(estado="aprobado").order_by(
        "-fecha_creacion"
    )
    contexto = {"herramientas": herramientas}
    return render(request, "herramientas/lista_herramientas.html", contexto)


@login_required
def subir_herramienta(request):
    if request.method == "POST":
        form = HerramientaForm(request.POST, request.FILES)
        if form.is_valid():
            herramienta = form.save(commit=False)
            herramienta.autor = request.user
            herramienta.estado = "pendiente"
            herramienta.save()
            return redirect("cursos:lista_herramientas")
    else:
        form = HerramientaForm()
    contexto = {"form": form}
    return render(request, "herramientas/subir_herramienta.html", contexto)


def lista_juegos(request):
    juegos = Juego.objects.filter(estado="aprobado").order_by("-fecha_creacion")
    contexto = {"juegos": juegos}
    return render(request, "juegos/lista_juegos.html", contexto)


@login_required
def subir_juego(request):
    if request.method == "POST":
        form = JuegoForm(request.POST, request.FILES)
        if form.is_valid():
            juego = form.save(commit=False)
            juego.autor = request.user
            juego.estado = "pendiente"
            juego.save()
            return redirect("cursos:lista_juegos")
    else:
        form = JuegoForm()
    contexto = {"form": form}
    return render(request, "juegos/subir_juego.html", contexto)


@login_required
def editar_herramienta(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, pk=herramienta_id)
    if request.user != herramienta.autor:
        return redirect("cursos:lista_herramientas")
    if request.method == "POST":
        form = HerramientaForm(request.POST, request.FILES, instance=herramienta)
        if form.is_valid():
            form.save()
            return redirect("cursos:lista_herramientas")
    else:
        form = HerramientaForm(instance=herramienta)
    contexto = {"form": form, "herramienta": herramienta}
    return render(request, "herramientas/editar_herramienta.html", contexto)


@login_required
def editar_juego(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    if request.user != juego.autor:
        return redirect("cursos:lista_juegos")
    if request.method == "POST":
        form = JuegoForm(request.POST, request.FILES, instance=juego)
        if form.is_valid():
            form.save()
            return redirect("cursos:lista_juegos")
    else:
        form = JuegoForm(instance=juego)
    contexto = {"form": form, "juego": juego}
    return render(request, "juegos/editar_juego.html", contexto)


@login_required
def eliminar_herramienta(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, pk=herramienta_id)
    if request.user == herramienta.autor or request.user.is_superuser:
        herramienta.delete()
    return redirect("cursos:lista_herramientas")


@login_required
def eliminar_juego(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    if request.user == juego.autor or request.user.is_superuser:
        juego.delete()
    return redirect("cursos:lista_juegos")


@login_required
def zona_practica(request, leccion_id):
    leccion = get_object_or_404(Leccion, pk=leccion_id)
    contexto = {"leccion": leccion}
    return render(request, "cursos/zona_practica.html", contexto)


@login_required
def track_click_herramienta(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, pk=herramienta_id)
    herramienta.click_count += 1
    herramienta.save()
    if herramienta.archivo:
        return redirect(herramienta.archivo.url)
    return redirect(herramienta.enlace)


@login_required
def track_click_juego(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    juego.click_count += 1
    juego.save()
    if juego.archivo:
        return redirect(juego.archivo.url)
    return redirect(juego.enlace)


def vista_perfil(request, username):
    perfil_usuario = get_object_or_404(User, username=username)
    posts = Post.objects.filter(autor=perfil_usuario).order_by("-fecha_publicacion")
    herramientas = Herramienta.objects.filter(autor=perfil_usuario).order_by(
        "-fecha_creacion"
    )
    juegos = Juego.objects.filter(autor=perfil_usuario).order_by("-fecha_creacion")
    xp = perfil_usuario.perfil.total_xp
    nivel = int(xp / 100) + 1
    xp_para_siguiente_nivel = nivel * 100
    progreso_nivel = int((xp % 100))
    contexto = {
        "perfil_usuario": perfil_usuario,
        "posts": posts,
        "herramientas": herramientas,
        "juegos": juegos,
        "nivel": nivel,
        "progreso_nivel": progreso_nivel,
        "xp_para_siguiente_nivel": xp_para_siguiente_nivel,
    }
    return render(request, "perfil/vista_perfil.html", contexto)


# --- ZONA DE PRÁCTICA (VERSIÓN FINAL CON SEGURIDAD CORRECTA) ---


@csrf_exempt
@require_POST
def execute_code(request):
    try:
        data = json.loads(request.body)
        code = data.get("code")

        executor_path = os.path.join(os.path.dirname(__file__), "executor.py")

        process = subprocess.Popen(
            ["python", executor_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = process.communicate(code, timeout=3)

        try:
            result = json.loads(stdout)
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "error": f"Error inesperado al ejecutar tu código. Intenta de nuevo. Detalles técnicos: {stderr}"
                },
                status=500,
            )

        if "error" in result:
            return JsonResponse({"error": result["error"]})
        else:
            return JsonResponse({"output": result["output"]})

    except subprocess.TimeoutExpired:
        process.kill()
        return JsonResponse(
            {
                "error": "La ejecución de tu código superó el tiempo límite de 3 segundos."
            }
        )
    except Exception as e:
        return JsonResponse({"error": f"Error del servidor: {str(e)}"}, status=500)


@csrf_exempt
@require_POST
@login_required
def validar_codigo(request):
    try:
        data = json.loads(request.body)
        leccion_id = data.get("leccion_id")
        codigo_usuario = data.get("code")

        try:
            leccion = Leccion.objects.get(pk=leccion_id)
            casos_prueba = leccion.casos_prueba.all()
        except Leccion.DoesNotExist:
            return JsonResponse({"error": "La lección no existe."}, status=404)

        if not casos_prueba:
            return JsonResponse(
                {"output": "Esta lección no tiene pruebas de validación."}
            )

        resultados = []
        pruebas_pasadas = 0

        # Ejecutar el código del usuario para verificar errores de sintaxis
        executor_path = os.path.join(os.path.dirname(__file__), "executor.py")

        try:
            process = subprocess.Popen(
                ["python", executor_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate(codigo_usuario, timeout=3)
            result = json.loads(stdout)
            if "error" in result:
                return JsonResponse({"error": f"Error en tu código: {result['error']}"})
        except subprocess.TimeoutExpired:
            process.kill()
            return JsonResponse(
                {"error": "La validación de tu código superó el tiempo límite."}
            )

        # Luego, ejecutar cada caso de prueba
        for caso in casos_prueba:
            try:
                codigo_completo = ""
                # Lógica corregida para el caso de prueba de salida directa
                if caso.expresion_a_evaluar == "Salida de consola directa":
                    codigo_completo = codigo_usuario
                else:
                    # Si no es un caso de salida directa, concatenamos el código
                    # con la expresión a evaluar para que el ejecutor la imprima
                    codigo_completo = (
                        f"{codigo_usuario}\n\nprint({caso.expresion_a_evaluar})"
                    )

                process = subprocess.Popen(
                    ["python", executor_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stdout, stderr = process.communicate(codigo_completo, timeout=3)

                result = json.loads(stdout)

                if "error" in result:
                    error_info = result["error"].splitlines()[-1]
                    resultados.append(
                        {
                            "expresion": caso.expresion_a_evaluar,
                            "esperado": caso.resultado_esperado,
                            "obtenido": f"Error: {error_info}",
                            "paso": False,
                        }
                    )
                    continue

                salida_obtenida = result["output"].strip()
                resultado_esperado = caso.resultado_esperado.strip()

                # Lógica de validación inteligente (se mantiene)
                paso_la_prueba = False
                patron_literal = r"([\{\[\(].*[\}\]\)])"
                match_obtenido = re.search(patron_literal, salida_obtenida)
                match_esperado = re.search(patron_literal, resultado_esperado)
                if match_obtenido and match_esperado:
                    try:
                        obj_obtenido = ast.literal_eval(match_obtenido.group(1))
                        obj_esperado = ast.literal_eval(match_esperado.group(1))
                        paso_la_prueba = obj_obtenido == obj_esperado
                    except (ValueError, SyntaxError):
                        paso_la_prueba = salida_obtenida.replace(
                            "\r\n", "\n"
                        ) == resultado_esperado.replace("\r\n", "\n")
                else:
                    paso_la_prueba = salida_obtenida.replace(
                        "\r\n", "\n"
                    ) == resultado_esperado.replace("\r\n", "\n")

                if paso_la_prueba:
                    pruebas_pasadas += 1

                resultados.append(
                    {
                        "expresion": caso.expresion_a_evaluar,
                        "esperado": resultado_esperado,
                        "obtenido": salida_obtenida,
                        "paso": paso_la_prueba,
                    }
                )

            except subprocess.TimeoutExpired:
                process.kill()
                resultados.append(
                    {
                        "expresion": caso.expresion_a_evaluar,
                        "esperado": caso.resultado_esperado,
                        "obtenido": "La ejecución de la prueba superó el tiempo límite.",
                        "paso": False,
                    }
                )
            except Exception as e:
                resultados.append(
                    {
                        "expresion": caso.expresion_a_evaluar,
                        "esperado": caso.resultado_esperado,
                        "obtenido": f"Error inesperado: {str(e)}",
                        "paso": False,
                    }
                )

        leccion_completada_ahora = False
        xp_ganados = 0
        if (
            pruebas_pasadas == len(casos_prueba)
            and not leccion.usuarios_completado.filter(pk=request.user.pk).exists()
        ):
            leccion.usuarios_completado.add(request.user)
            perfil = request.user.perfil
            perfil.total_xp += leccion.puntos_xp
            perfil.save()
            leccion_completada_ahora = True
            xp_ganados = leccion.puntos_xp

        return JsonResponse(
            {
                "pruebas_pasadas": pruebas_pasadas,
                "total_pruebas": len(casos_prueba),
                "resultados_detallados": resultados,
                "leccion_completada_ahora": leccion_completada_ahora,
                "xp_ganados": xp_ganados,
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
