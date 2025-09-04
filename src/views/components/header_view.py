import tkinter as tk

class Header(tk.Frame):
    def __init__(self, parent, on_registro, on_exportar, on_salir):
        super().__init__(parent, bg="#f0f0f0", height=80)
        self.pack(fill="x")

        # Logo
        tk.Label(self, text="LOGO", bg="#d0d0d0", width=10, height=4).pack(side="left", padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(side="right", padx=10)

        tk.Button(btn_frame, text="Registro", command = on_registro, bg="#7de986").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Exportar", command = on_exportar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Salir", command = on_salir, bg="#d9534f", fg="white").pack(side="left", padx=5)
        