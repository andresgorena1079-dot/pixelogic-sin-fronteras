import os

from django.conf import settings
from django.db import IntegrityError

from cursos.models import Curso, Leccion, Modulo


def run():
    print(
        "Iniciando la carga de datos del curso 'Python Sin Fronteras' desde archivos HTML..."
    )

    # Define la ruta base donde están tus módulos
    base_path = os.path.join(settings.BASE_DIR, "modules")

    # --- 1. CREAR EL CURSO PRINCIPAL ---
    try:
        curso_python, created = Curso.objects.get_or_create(
            titulo="Python Sin Fronteras",
            defaults={
                "descripcion": "Un viaje completo para dominar Python desde cero."
            },
        )
        if created:
            print(f"Curso '{curso_python.titulo}' creado exitosamente.")
        else:
            print(f"Curso '{curso_python.titulo}' ya existe. ¡Continuando!")
    except IntegrityError as e:
        print(f"Error al crear el curso: {e}")
        return

    # --- 2. CARGAR MÓDULOS Y LECCIONES DINÁMICAMENTE ---
    for module_dir in sorted(os.listdir(base_path)):
        if module_dir.startswith("module_"):
            module_name = module_dir.replace("module_", "").replace("_", " ").title()

            # Crear el Módulo
            try:
                modulo, created = Modulo.objects.get_or_create(
                    curso=curso_python,
                    titulo=f"Módulo {module_name}",
                    defaults={"descripcion": f"Descripción del {module_name}"},
                )
                if created:
                    print(f"  Módulo '{modulo.titulo}' creado.")

                # Cargar Lecciones
                module_path = os.path.join(base_path, module_dir)
                for lesson_file in sorted(os.listdir(module_path)):
                    if lesson_file.endswith(".html"):
                        lesson_title = (
                            lesson_file.replace(".html", "").replace("_", " ").title()
                        )
                        lesson_order = int(lesson_file.split("_")[0])

                        with open(
                            os.path.join(module_path, lesson_file),
                            "r",
                            encoding="utf-8",
                        ) as f:
                            lesson_content = f.read()

                        leccion, leccion_created = Leccion.objects.get_or_create(
                            modulo=modulo,
                            titulo=lesson_title,
                            orden=lesson_order,
                            defaults={"contenido_html": lesson_content},
                        )
                        if leccion_created:
                            print(f"    - Lección '{leccion.titulo}' creada.")

            except IntegrityError as e:
                print(f"Error al procesar {module_dir}: {e}")

    print("Carga de datos finalizada.")
