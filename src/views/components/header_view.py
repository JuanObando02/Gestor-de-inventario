import tkinter as tk

class Header(tk.Frame):


    def __init__(self, ventana, crear_producto, bt_registrar, bt_exportar, bt_salir):
        super().__init__(ventana, bg="#c1dd36", height=80)
        self.pack(fill="x")
        # la ventana se expande horizontalmente y se mantiene en la parte superior con fill="x"

        # Logo
        tk.Label(self, text="LOGO", bg="#2b03db", width=10, height=4).pack(side="left", padx=10, pady=10)

        # Botones
        ventana_botones = tk.Frame(self, bg="#0485d0")
        ventana_botones.pack(side="right", padx=10)
        # ventada secundaria con los botones alineados a la derecha 

        tk.Button(ventana_botones, text="Nuevo Producto", command = crear_producto, bg="#1806db").pack(side="left", padx=5)
        tk.Button(ventana_botones, text="Registro", command = bt_registrar, bg="#7de986")            .pack(side="left", padx=5)
        tk.Button(ventana_botones, text="Exportar", command = bt_exportar,  bg="#ffffff")            .pack(side="left", padx=5)
        tk.Button(ventana_botones, text="Salir",    command = bt_salir,     bg="#1a1414", fg="white").pack(side="left", padx=5)
        