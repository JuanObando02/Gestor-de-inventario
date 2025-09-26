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
        self.iconphoto(False, tk.PhotoImage(file="assets/images/Logo_icon.png"))

        # Canvas principal
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#B6B6B6")
        self.canvas.pack(fill="both", expand=True)

        # Fondo con logo
        try:
            logo = Image.open("assets/images/Logo_con_nombre_100x126.png").convert("RGBA")
            logo = logo.resize((200, 200), Image.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(logo)
            self.logo_item = self.canvas.create_image(0, 0, image=self.logo_tk, anchor="center")
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            self.logo_item = None

        # === Usuario ===
        self.text_usuario = self.canvas.create_text(0, 0, text="Usuario:", fill="black", font=("Arial", 12, "bold"))
        self.entry_usuario = tk.Entry(self, width=20, font=("Arial", 12))
        self.entry_usuario_item = self.canvas.create_window(0, 0, window=self.entry_usuario)

        # === Contraseña ===
        self.text_password = self.canvas.create_text(0, 0, text="Contraseña:", fill="black", font=("Arial", 12, "bold"))
        self.entry_password = tk.Entry(self, show="*", width=20, font=("Arial", 12))
        self.entry_password_item = self.canvas.create_window(0, 0, window=self.entry_password)

        # === Rol ===
        self.text_rol = self.canvas.create_text(0, 0, text="Rol:", fill="black", font=("Arial", 12, "bold"))
        self.rol_var = tk.StringVar(value="empleado")
        roles = ["administrador", "empleado"]
        self.rol = ttk.Combobox(self, textvariable=self.rol_var, values=roles, state="readonly", width=18)
        self.rol_item = self.canvas.create_window(0, 0, window=self.rol)

        # Botón crear
        self.btn_crear = tk.Button(self, text="Crear", command=self.crear_usuario,
                                   bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.btn_item = self.canvas.create_window(0, 0, window=self.btn_crear)

        # Reubicar al cambiar tamaño de ventana
        self.bind("<Configure>", self.reubicar_elementos)

        # Atajo Enter para crear usuario
        self.bind("<Return>", lambda event: self.crear_usuario())

    def reubicar_elementos(self, event=None):
        """Mantener todo centrado al cambiar tamaño de ventana"""
        w = self.winfo_width()
        h = self.winfo_height()

        cx, cy = w // 2, h // 2  # centro ventana

        # Logo centrado
        if self.logo_item:
            self.canvas.coords(self.logo_item, cx, cy)

        # Usuario
        self.canvas.coords(self.text_usuario, cx - 120, cy - 80)
        self.canvas.coords(self.entry_usuario_item, cx + 30, cy - 80)

        # Contraseña
        self.canvas.coords(self.text_password, cx - 120, cy - 40)
        self.canvas.coords(self.entry_password_item, cx + 30, cy - 40)

        # Rol
        self.canvas.coords(self.text_rol, cx - 120, cy)
        self.canvas.coords(self.rol_item, cx + 30, cy)

        # Botón
        self.canvas.coords(self.btn_item, cx, cy + 60)

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
