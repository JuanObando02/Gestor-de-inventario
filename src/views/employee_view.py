import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_usuario

class VentanaEmpleado(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear Nuevo Empleado")
        self.geometry("350x250")
        self.centrar_ventana(350, 250)
        self.config(bg="white")

        # === Usuario ===
        tk.Label(self, text="Usuario:", bg="white").pack(pady=5)
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack(pady=5)

        # === Contraseña ===
        tk.Label(self, text="Contraseña:", bg="white").pack(pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        # === Rol ===
        tk.Label(self, text="Rol:", bg="white").pack(pady=5)
        self.rol_var = tk.StringVar(value="empleado")
        roles = ["administrador", "empleado"]
        self.rol = ttk.Combobox(self, textvariable=self.rol_var, values=roles, state="readonly")
        self.rol.pack(pady=5)

        # Botón crear
        tk.Button(self, text="Crear", command=self.crear_usuario).pack(pady=20)
        self.bind("<Return>", lambda event: self.crear_usuario())

    def centrar_ventana(self, ancho=300, alto=400):
        """Centrar ventana en la pantalla"""
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_usuario(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        rol = self.rol.get()

        if not usuario or not password or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            controlador_usuario.insert_user(usuario, password, rol)
            messagebox.showinfo("Éxito", "Empleado creado correctamente")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear empleado: {e}")
