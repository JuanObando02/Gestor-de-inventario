import os
from PIL import Image

# Carpeta actual donde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


imagen = Image.open("assets/images/Logo_blanco.png")
imagen = imagen.resize((80, 100), Image.LANCZOS)  
imagen.save("assets/images/Logo_blanco_80x100.png", optimize=True)

