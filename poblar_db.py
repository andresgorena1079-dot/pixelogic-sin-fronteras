# poblar_db.py
import os

import django

# Configuración inicial para que el script reconozca el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixelogic.settings")
django.setup()

# Ahora podemos importar nuestros modelos
from cursos.models import Curso, Leccion, Modulo

# --- DATOS DEL CURSO ---

# Diccionario con las descripciones que preparamos en el Paso 1
MODULOS_DATA = {
    "module_01_fundamentos": {
        "titulo": "Módulo 1: Fundamentos de Python",
        "descripcion": "Sienta las bases de tu viaje en la programación. Aprenderás a configurar tu entorno, la sintaxis básica del lenguaje, los tipos de datos, los operadores y cómo controlar el flujo de tus programas con funciones y condicionales.",
    },
    "module_02_estructuras_de_datos": {
        "titulo": "Módulo 2: Estructuras de Datos en Profundidad",
        "descripcion": "Domina las colecciones de datos de Python. Exploraremos a fondo las listas, tuplas, diccionarios y conjuntos, aprendiendo sus métodos y cuándo usar cada uno para manejar información de manera eficiente.",
    },
    "module_03_poo": {
        "titulo": "Módulo 3: Programación Orientada a Objetos (POO)",
        "descripcion": "Aprende el paradigma que impulsa el software moderno. Entenderás qué son las clases y los objetos, y cómo usar los pilares de la POO como la herencia, el polimorfismo y el encapsulamiento para crear código robusto y reutilizable.",
    },
    "module_04_errores_y_archivos": {
        "titulo": "Módulo 4: Manejo de Errores y Archivos",
        "descripcion": "Prepara tus programas para el mundo real. Aprenderás a anticipar y gestionar errores con excepciones para evitar que tu aplicación se detenga, y a leer y escribir datos en archivos para que tu información persista.",
    },
    "module_05_temas_avanzados": {
        "titulo": "Módulo 5: Temas Avanzados de Python",
        "descripcion": "Eleva tu nivel de Python con conceptos poderosos. Descubrirás técnicas elegantes como la comprensión de listas y las funciones lambda, la eficiencia de los generadores y decoradores, y el poder de la programación asincrónica.",
    },
    "module_06_libreria_estandar": {
        "titulo": "Módulo 6: La Librería Estándar y Expresiones Regulares",
        "descripcion": "Explora las 'baterías incluidas' de Python. Conocerás los módulos esenciales para interactuar con el sistema operativo, y aprenderás a usar expresiones regulares para encontrar y manipular patrones en texto como un profesional.",
    },
    "module_07_ecosistema_profesional": {
        "titulo": "Módulo 7: Ecosistema y Desarrollo Profesional",
        "descripcion": "Da el salto al desarrollo profesional con las herramientas más populares del ecosistema. Tendrás una introducción a librerías fundamentales para el análisis de datos como Pandas y la creación de aplicaciones web.",
    },
}

# --- SCRIPT DE POBLACIÓN ---


def poblar_base_de_datos():
    print("Iniciando el script de población...")

    # Limpiamos los cursos existentes para evitar duplicados
    Curso.objects.all().delete()
    print("Cursos antiguos eliminados.")

    # Creamos el curso principal
    curso_python = Curso.objects.create(
        titulo="Python Sin Fronteras",
        descripcion="Un viaje completo para dominar Python desde cero, cubriendo desde los fundamentos hasta temas avanzados y profesionales.",
    )
    print(f"Curso '{curso_python.titulo}' creado.")

    # Ruta a la carpeta que contiene los módulos
    ruta_modulos_base = "modules"

    # Obtenemos la lista de carpetas de módulos y las ordenamos
    carpetas_modulos = sorted(os.listdir(ruta_modulos_base))

    for nombre_carpeta_modulo in carpetas_modulos:
        if nombre_carpeta_modulo in MODULOS_DATA:
            # Creamos el Módulo en la base de datos
            datos_modulo = MODULOS_DATA[nombre_carpeta_modulo]
            modulo_actual = Modulo.objects.create(
                curso=curso_python,
                titulo=datos_modulo["titulo"],
                descripcion=datos_modulo["descripcion"],
            )
            print(f"  Módulo '{modulo_actual.titulo}' creado.")

            # Ruta a la carpeta de lecciones
            ruta_lecciones = os.path.join(ruta_modulos_base, nombre_carpeta_modulo)
            archivos_lecciones = sorted(os.listdir(ruta_lecciones))

            for nombre_archivo_leccion in archivos_lecciones:
                if nombre_archivo_leccion.endswith(".html"):
                    # Extraemos el orden y el título del nombre del archivo
                    partes = nombre_archivo_leccion.replace(".html", "").split("_", 1)
                    orden = int(partes[0])
                    titulo_leccion = partes[1].replace("_", " ").capitalize()

                    # Leemos el contenido HTML del archivo
                    try:
                        with open(
                            os.path.join(ruta_lecciones, nombre_archivo_leccion),
                            "r",
                            encoding="utf-8",
                        ) as f:
                            contenido_html = f.read()
                    except Exception as e:
                        print(
                            f"    ERROR al leer el archivo {nombre_archivo_leccion}: {e}"
                        )
                        contenido_html = "<p>Error al cargar el contenido.</p>"

                    # Creamos la Lección en la base de datos
                    Leccion.objects.create(
                        modulo=modulo_actual,
                        titulo=titulo_leccion,
                        contenido_html=contenido_html,
                        orden=orden,
                    )
                    print(f"    - Lección '{titulo_leccion}' creada.")

    print("\n¡Población de la base de datos completada con éxito!")


# --- EJECUTAR EL SCRIPT ---
if __name__ == "__main__":
    poblar_base_de_datos()
