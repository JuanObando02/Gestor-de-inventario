import tkinter as tk
import os
from PIL import Image, ImageTk
from src.utils.path_utils import resource_path

class Header(tk.Frame):

    def __init__(self, ventana, crear_empleado=None, ver_empleados=None, crear_producto=None, bt_registrar=None, bt_cerrar_sesion=None, importar_csv=None, exportar_archivo=None):
        super().__init__(ventana, bg="#357bb7", height=80)
        self.pack(fill="x")
        logo_path = resource_path("assets/images/Logo_blanco_80x100.png")
        self.logo_img = ImageTk.PhotoImage(Image.open(logo_path))

        tk.Label(self, image=self.logo_img, bg="#357bb7").pack(side="left", padx=10, pady=10)

        # Botones
        ventana_botones = tk.Frame(self, bg="#357bb7")
        ventana_botones.pack(side="right", padx=10)
        # frame secundario con los botones alineados a la derecha 

        if crear_empleado:
            #--- Menú para la gestión de empleados (crear y ver lista)---
            Menu_empleados = tk.Menubutton(ventana_botones, text="Gestión de Empleados", bg="#ffffff", relief="raised")
            Menu_empleados.menu = tk.Menu(Menu_empleados, tearoff=0)
            Menu_empleados["menu"] = Menu_empleados.menu
            Menu_empleados.menu.add_command(label="Crear nuevo empleado", command=crear_empleado)
            Menu_empleados.menu.add_command(label="Lista de empleados", command=ver_empleados)
            Menu_empleados.pack(side="left", padx=5)
            
        tk.Button(ventana_botones, text="Nuevo Producto", command = crear_producto, bg="#ffffff").pack(side="left", padx=5)
        tk.Button(ventana_botones, text="Registro", command = bt_registrar, bg="#ffffff")        .pack(side="left", padx=5)

        #--- Menú para la gestión de archivos (importar y exportar)---
        Menu_archivos = tk.Menubutton(ventana_botones, text="Gestión de Archivos", bg="#ffffff", relief="raised")
        Menu_archivos.menu = tk.Menu(Menu_archivos, tearoff=0)
        Menu_archivos["menu"] = Menu_archivos.menu
        Menu_archivos.menu.add_command(label="Importar Archivo", command=importar_csv)
        Menu_archivos.menu.add_command(label="Exportar Archivo", command=exportar_archivo)
        Menu_archivos.pack(side="left", padx=5)

        # boton cerrar sesion volver a login
        tk.Button(ventana_botones, text="Cerrar Sesión",    command = bt_cerrar_sesion,     bg="#357BB7", fg="white").pack(side="left", padx=5)