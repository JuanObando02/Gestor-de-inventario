import tkinter as tk
import os
from PIL import Image, ImageTk

class Header(tk.Frame):


    def __init__(self, ventana, bt_empleado, crear_producto, bt_registrar, bt_cerrar_sesion, importar_csv, exportar_archivo):
        super().__init__(ventana, bg="#357bb7", height=80)
        self.pack(fill="x")
        # la ventana se expande horizontalmente y se mantiene en la parte superior con fill="x"

        # --- Logo ---
        imagen = Image.open("assets/images/Logo_blanco_80x100.png")
        self.logo_img = ImageTk.PhotoImage(imagen)

        tk.Label(self, image=self.logo_img, bg="#357bb7").pack(side="left", padx=10, pady=10)

        # Botones
        ventana_botones = tk.Frame(self, bg="#357bb7")
        ventana_botones.pack(side="right", padx=10)
        # ventada secundaria con los botones alineados a la derecha 

        if bt_empleado:
            tk.Button(ventana_botones, text="Nuevo Empleado", command = bt_empleado,  bg="#ffffff").pack(side="left", padx=5)
            
        tk.Button(ventana_botones, text="Nuevo Producto", command = crear_producto, bg="#ffffff").pack(side="left", padx=5)
        tk.Button(ventana_botones, text="Registro", command = bt_registrar, bg="#ffffff")            .pack(side="left", padx=5)

        #--- Menú para la gestión de archivos (importar y exportar)---
        gestion_archivos_btn = tk.Menubutton(ventana_botones, text="Gestión de Archivos", bg="#ffffff", relief="raised")
        gestion_archivos_btn.menu = tk.Menu(gestion_archivos_btn, tearoff=0)
        gestion_archivos_btn["menu"] = gestion_archivos_btn.menu

        gestion_archivos_btn.menu.add_command(label="Importar CSV", command=importar_csv)
        gestion_archivos_btn.menu.add_command(label="Exportar CSV", command=exportar_archivo)

        gestion_archivos_btn.pack(side="left", padx=5)

        
        tk.Button(ventana_botones, text="Cerrar Sesión",    command = bt_cerrar_sesion,     bg="#357BB7", fg="white").pack(side="left", padx=5)

        