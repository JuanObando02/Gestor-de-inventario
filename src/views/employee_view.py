import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_usuario
from PIL import Image, ImageTk
from src.utils.path_utils import resource_path

class VentanaEmpleado(tk.Toplevel):
    def __init__(self, parent, usuario=None):
        super().__init__(parent)
        self.usuario_a_editar = usuario  # None si es nuevo
        self.title("Crear Nuevo Empleado" if not usuario else f"Editar Empleado: {usuario}")
        self.geometry("350x285")
        self.centrar_ventana(350, 285)
        icon_path = resource_path("assets/images/Logo_icon.png")
        self.iconphoto(False, tk.PhotoImage(file=icon_path))

        # Canvas principal
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#B6B6B6")
        self.canvas.pack(fill="both", expand=True)

        # Fondo con logo
        try:
            self.logo_tk = ImageTk.PhotoImage(Image.open("assets/images/Logo_BG.png").convert("RGBA"))
            logo_bg_path = resource_path("assets/images/Logo_BG.png")
            self.logo_tk = ImageTk.PhotoImage(Image.open(logo_bg_path).convert("RGBA"))
            self.logo_item = self.canvas.create_image(0, 0, image=self.logo_tk, anchor="center")
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            self.logo_item = None

        # Usuario
        self.text_usuario = self.canvas.create_text(0, 0, text="Usuario:", fill="black", font=("Arial", 12, "bold"))
        self.entry_usuario = tk.Entry(self, width=20, font=("Arial", 12))
        self.entry_usuario_item = self.canvas.create_window(0, 0, window=self.entry_usuario)

        # Contraseña
        self.text_password = self.canvas.create_text(0, 0, text="Contraseña:", fill="black", font=("Arial", 12, "bold"))
        self.entry_password = tk.Entry(self, show="*", width=20, font=("Arial", 12))
        self.entry_password_item = self.canvas.create_window(0, 0, window=self.entry_password)

        # Rol
        self.text_rol = self.canvas.create_text(0, 0, text="Rol:", fill="black", font=("Arial", 12, "bold"))
        self.rol_var = tk.StringVar(value="empleado")
        roles = ["administrador", "empleado"]
        self.rol = ttk.Combobox(self, textvariable=self.rol_var, values=roles, state="readonly", width=18)
        self.rol_item = self.canvas.create_window(0, 0, window=self.rol)

        # Botón Crear/Actualizar
        btn_text = "Crear" if not usuario else "Actualizar"
        self.btn_crear = tk.Button(
            self,
            text=btn_text,
            command=self.crear_o_actualizar_usuario,
            bg="#12A617",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.btn_item = self.canvas.create_window(0, 0, window=self.btn_crear)

        # Reubicar al cambiar tamaño de ventana
        self.bind("<Configure>", self.reubicar_elementos)
        self.bind("<Return>", lambda event: self.crear_o_actualizar_usuario())

        # Si es edición, precargar datos
        if usuario:
            self.entry_usuario.insert(0, usuario)
            user_obj = controlador_usuario.get_user(usuario)
            if user_obj:
                self.rol_var.set(user_obj.rol)

    def crear_o_actualizar_usuario(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        rol = self.rol.get()

        if not usuario or not rol:
            messagebox.showerror("Error", "Usuario y rol son obligatorios")
            return

        try:
            if self.usuario_a_editar:  # actualizar
                controlador_usuario.update_user(self.usuario_a_editar, password, rol)
                messagebox.showinfo("Éxito", f"Empleado {usuario} actualizado")
            else:  # crear
                if not password:
                    messagebox.showerror("Error", "La contraseña es obligatoria")
                    return
                controlador_usuario.insert_user(usuario, password, rol)
                messagebox.showinfo("Éxito", f"Empleado {usuario} creado")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reubicar_elementos(self, event=None):
        w = self.winfo_width()
        h = self.winfo_height()
        cx, cy = w // 2, h // 2

        if self.logo_item:
            self.canvas.coords(self.logo_item, cx, cy)

        self.canvas.coords(self.text_usuario, cx - 120, cy - 80)
        self.canvas.coords(self.entry_usuario_item, cx + 30, cy - 80)
        self.canvas.coords(self.text_password, cx - 120, cy - 40)
        self.canvas.coords(self.entry_password_item, cx + 30, cy - 40)
        self.canvas.coords(self.text_rol, cx - 120, cy)
        self.canvas.coords(self.rol_item, cx + 30, cy)
        self.canvas.coords(self.btn_item, cx, cy + 60)

    def centrar_ventana(self, ancho=300, alto=400):
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")


class VentanaListaEmpleados(tk.Toplevel):
    """Lista de empleados con acciones de editar y eliminar"""
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        self.title("Lista de Empleados")
        self.geometry("450x300")
        self.centrar_ventana(450, 300)
        self.iconphoto(False, tk.PhotoImage(file="assets/images/Logo_icon.png"))

        self.tree = ttk.Treeview(self, columns=("Usuario", "Rol", "Acciones"), show="headings")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Rol", text="Rol")
        self.tree.heading("Acciones", text="Acciones")
        self.tree.column("Usuario", width=150)
        self.tree.column("Rol", width=100)
        self.tree.column("Acciones", width=180, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.cargar_usuarios()

    def cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.usuarios = controlador_usuario.list_users()  # [(id, usuario, rol)]
        for u in self.usuarios:
            self.tree.insert("", "end", values=(u[1], u[2], "Editar | Eliminar"))

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not item or col != "#3":
            return

        empleado = self.tree.item(item, "values")
        bbox = self.tree.bbox(item, col)
        if not bbox:
            return

        click_x = event.x - bbox[0]
        usuario = empleado[0]

        # Buscar id_usuario
        user_id = next((u[0] for u in self.usuarios if u[1] == usuario), None)

        if click_x < bbox[2] // 2:
            # Editar
            VentanaEmpleado(self, usuario=usuario)
        else:
            # Eliminar
            if self.current_user.role != "admin":
                messagebox.showerror("Permiso denegado")
                return
            if messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar {usuario}?"):
                if user_id:
                    controlador_usuario.delete_user(user_id)
                    messagebox.showinfo("Éxito", f"Empleado {usuario} eliminado.")
                    self.cargar_usuarios()

    def centrar_ventana(self, ancho=450, alto=300):
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
