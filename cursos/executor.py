import ast
import io
import json
import os
import sys
import traceback


def block_network_access():
    """
    Bloquea las funciones de red más comunes.
    """
    # Lista negra de módulos que no deben ser importados.
    banned_modules = ["socket", "urllib", "http", "requests", "asyncio"]
    for module in banned_modules:
        sys.modules[module] = None


def main():
    """
    Ejecuta el código de Python de forma segura.
    Lee el código de la entrada estándar, lo ejecuta en un entorno limitado
    y devuelve la salida o el error como JSON.
    """
    # Llama a la función de seguridad antes de ejecutar cualquier cosa
    # Nota: El módulo 'resource' para límites de CPU/memoria es solo para Unix.
    # El 'timeout' en subprocess.communicate() en views.py ya maneja la mayoría
    # de los ataques de agotamiento de recursos.
    block_network_access()

    try:
        user_code = sys.stdin.read()

        # Analiza el código para detectar importaciones prohibidas
        node = ast.parse(user_code)
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Import) or isinstance(sub_node, ast.ImportFrom):
                for name in sub_node.names:
                    # Lista blanca de módulos permitidos
                    if name.name not in ["math", "re"]:
                        raise ImportError(f"Importación no permitida: {name.name}")

        # Entorno seguro con una lista blanca de funciones
        safe_builtins = {
            "abs": abs,
            "max": max,
            "min": min,
            "sum": sum,
            "print": print,
            "range": range,
            "list": list,
            "dict": dict,
            "str": str,
            "int": int,
            "float": float,
            "tuple": tuple,
            "len": len,
            "zip": zip,
            "enumerate": enumerate,
            "sorted": sorted,
            "isinstance": isinstance,
        }

        # Agrega una lista blanca de módulos
        safe_globals = {
            "__builtins__": safe_builtins,
            "re": __import__("re"),
            "math": __import__("math"),
        }

        # Redirige la salida estándar (print)
        old_stdout = sys.stdout
        sys.stdout = output_buffer = io.StringIO()

        # Ejecuta el código
        exec(user_code, safe_globals, safe_globals)

        sys.stdout = old_stdout
        print(json.dumps({"output": output_buffer.getvalue()}))

    except Exception:
        sys.stdout = old_stdout
        error_info = traceback.format_exc()
        print(json.dumps({"error": error_info}))


if __name__ == "__main__":
    main()
