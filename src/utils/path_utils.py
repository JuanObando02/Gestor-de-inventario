import os, sys

def resource_path(relative_path):
    """Obtiene ruta al recurso (funciona en dev y en onedir)"""
    try:
        base_path = sys._MEIPASS   # si es onefile
    except Exception:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))  # carpeta del exe

    return os.path.join(base_path, relative_path)