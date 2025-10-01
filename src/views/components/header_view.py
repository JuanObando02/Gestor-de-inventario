import tkinter as tk
import os
from PIL import Image, ImageTk

class Header(tk.Frame):


    def __init__(self, ventana, bt_empleado, crear_producto, bt_registrar, bt_exportar, bt_cerrar_sesion, importar_csv):
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
        tk.Button(ventana_botones, text="Exportar", command = bt_exportar,  bg="#ffffff")            .pack(side="left", padx=5)
        tk.Button(self, text="Importar CSV", command = importar_csv, bg = "#ffffff")                 .pack(side="left", padx=5)
        tk.Button(ventana_botones, text="Salir",    command = bt_salir,     bg="#357BB7", fg="white").pack(side="left", padx=5)

        