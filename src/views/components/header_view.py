import tkinter as tk
import os
from PIL import Image, ImageTk
from src.utils.path_utils import resource_path

class Header(tk.Frame):


    def __init__(self, ventana, bt_empleado=None, crear_empleado=None, ver_empleados=None, crear_producto=None, bt_registrar=None, bt_cerrar_sesion=None, importar_csv=None, exportar_archivo=None):
        super().__init__(ventana, bg="#357bb7", height=80)
        self.pack(fill="x")
        # la ventana se expande horizontalmente y se mantiene en la parte superior con fill="x"

        # --- Logo ---
        logo_path = resource_path("assets/images/Logo_blanco_80x100.png")
        imagen = Image.open(logo_path)
        self.logo_img = ImageTk.PhotoImage(imagen)

        tk.Label(self, image=self.logo_img, bg="#357bb7").pack(side="left", padx=10, pady=10)

        # Botones
        ventana_botones = tk.Frame(self, bg="#357bb7")
        ventana_botones.pack(side="right", padx=10)
        # ventada secundaria con los botones alineados a la derecha 

        if bt_empleado:
            #--- Menú para la gestión de empleados (crear y ver lista)---
            gestion_empleados_btn = tk.Menubutton(ventana_botones, text="Gestión de Empleados", bg="#ffffff", relief="raised")
            gestion_empleados_btn.menu = tk.Menu(gestion_empleados_btn, tearoff=0)
            gestion_empleados_btn["menu"] = gestion_empleados_btn.menu

            if crear_empleado:
                gestion_empleados_btn.menu.add_command(label="Crear nuevo empleado", command=crear_empleado)
            if ver_empleados:
                gestion_empleados_btn.menu.add_command(label="Lista de empleados", command=ver_empleados)
            gestion_empleados_btn.pack(side="left", padx=5)
            
        tk.Button(ventana_botones, text="Nuevo Producto", command = crear_producto, bg="#ffffff").pack(side="left", padx=5)
        tk.Button(ventana_botones, text="Registro", command = bt_registrar, bg="#ffffff")            .pack(side="left", padx=5)

        #--- Menú para la gestión de archivos (importar y exportar)---
        gestion_archivos_btn = tk.Menubutton(ventana_botones, text="Gestión de Archivos", bg="#ffffff", relief="raised")
        gestion_archivos_btn.menu = tk.Menu(gestion_archivos_btn, tearoff=0)
        gestion_archivos_btn["menu"] = gestion_archivos_btn.menu

        gestion_archivos_btn.menu.add_command(label="Importar Archivo", command=importar_csv)
        gestion_archivos_btn.menu.add_command(label="Exportar Archivo", command=exportar_archivo)
        gestion_archivos_btn.pack(side="left", padx=5)

        
        tk.Button(ventana_botones, text="Cerrar Sesión",    command = bt_cerrar_sesion,     bg="#357BB7", fg="white").pack(side="left", padx=5)