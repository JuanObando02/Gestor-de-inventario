import os
from PIL import Image, ImageTk

# Carpeta actual donde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


imagen = Image.open("assets/images/Logo_con_nombre.png").convert("RGBA")
imagen = imagen.resize((200, 252), Image.LANCZOS)  
imagen.save("assets/images/Loco_BG.png", optimize=True)

