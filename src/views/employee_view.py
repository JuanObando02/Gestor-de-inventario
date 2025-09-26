import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_usuario
from PIL import Image, ImageTk

class VentanaEmpleado(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear Nuevo Empleado")
        self.geometry("350x250")
        self.centrar_ventana(350, 250)
        self.config(bg="white")
        self.iconphoto(False, tk.PhotoImage(file="assets/images/Logo_icon.png"))
        self.config(bg="#B6B6B6")
         # Fondo con imagen/logo
        # =====================
        try:
            logo = Image.open("assets/images/Logo_con_nombre_100x126.png").convert("RGBA")  # logo con transparencia
            logo = logo.resize((200, 200), Image.LANCZOS)  # Ajustar tamaño
            # Crear un nuevo canal alfa con menos opacidad
            
            self.logo_tk = ImageTk.PhotoImage(logo)
            
            # Colocar en la ventana
            self.bg_label = tk.Label(self, image=self.logo_tk, bg="#B6B6B6")
            self.bg_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")

        # Frame para los widgets encima del fondo
        frame = tk.Frame(self, bg="#B6B6B6")
        frame.place(relx=0.5, rely=0.5, anchor="center")

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
