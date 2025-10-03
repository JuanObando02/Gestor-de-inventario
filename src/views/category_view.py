import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.controllers import controlador_categoria
from PIL import Image, ImageTk
from src.utils.path_utils import resource_path

# === Ventana para gestionar categorías ===
class VentanaCategorias(tk.Toplevel):
    def __init__(self, parent, on_update_callback):
        super().__init__(parent, bg="#B6B6B6")
        self.title("Gestionar Categorías")
        self.geometry("400x350")
        self.on_update_callback = on_update_callback
        self.centrar_ventana(400, 350)
        icon_path = resource_path("assets/images/Logo_icon.png")
        self.iconphoto(False, tk.PhotoImage(file=icon_path))

        # === Canvas principal ===
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#B6B6B6")
        self.canvas.pack(fill="both", expand=True)

        # === Fondo con logo ===
        try:
            logo_bg_path = resource_path("assets/images/Logo_BG.png")
            self.logo_tk = ImageTk.PhotoImage(Image.open(logo_bg_path).convert("RGBA"))
            self.logo_item = self.canvas.create_image(0, 0, image=self.logo_tk, anchor="center")
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            self.logo_item = None

        # === Widgets sobre el canvas ===
        self.text_lista = self.canvas.create_text(0, 0, text="Categorías:", fill="black", font=("Arial", 12, "bold"))
        self.lista = tk.Listbox(self, width=30, height=10)
        self.lista_item = self.canvas.create_window(0, 0, window = self.lista)

        self.btn_agregar = tk.Button(self, text="Agregar", bg = "#12A617", fg="white", command = self.agregar_categoria)
        self.btn_agregar_item = self.canvas.create_window(0, 0, window = self.btn_agregar)

        self.btn_editar = tk.Button(self, text="Editar", bg = "#D58B01", fg="black", command = self.editar_categoria)
        self.btn_editar_item = self.canvas.create_window(0, 0, window = self.btn_editar)

        self.btn_eliminar = tk.Button(self, text="Eliminar", bg= "#B02020", fg="white", command = self.eliminar_categoria)
        self.btn_eliminar_item = self.canvas.create_window(0, 0, window = self.btn_eliminar)

        # Cargar categorías
        self.cargar_categorias()

        # Reposicionar al cambiar tamaño
        self.bind("<Configure>", self.reubicar_elementos)

    def centrar_ventana(self, ancho=300, alto=400):
        """Centrar ventana en la pantalla"""
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def reubicar_elementos(self, event=None):
        """Mantener todo centrado en la ventana"""
        w = self.winfo_width()
        h = self.winfo_height()
        cx, cy = w // 2, h // 2

        # Logo centrado
        if self.logo_item:
            self.canvas.coords(self.logo_item, cx, cy)

        # Lista
        self.canvas.coords(self.text_lista, cx, cy - 120)
        self.canvas.coords(self.lista_item, cx, cy - 50)

        # Botones
        self.canvas.coords(self.btn_agregar_item, cx - 80, cy + 90)
        self.canvas.coords(self.btn_editar_item, cx, cy + 90)
        self.canvas.coords(self.btn_eliminar_item, cx + 80, cy + 90)

    def cargar_categorias(self):
        """Cargar categorías desde la base de datos"""
        self.lista.delete(0, tk.END)

        categorias = controlador_categoria.get_all_categorias()
        for c in categorias:
            self.lista.insert(tk.END, f"{c[0]} - {c[1]}")

    def agregar_categoria(self):
        nombre = simpledialog.askstring("Nueva categoría", "Ingrese el nombre:")

        if nombre:
            controlador_categoria.add_categoria(nombre)
            self.cargar_categorias()
            self.on_update_callback()

    def editar_categoria(self):
        sel = self.lista.curselection()

        if not sel:
            messagebox.showwarning("Atención", "Seleccione una categoría.")
            return
        
        cat_text = self.lista.get(sel[0])
        cat_id = int(cat_text.split(" - ")[0])
        nuevo_nombre = simpledialog.askstring("Editar categoría", "Nuevo nombre:")

        if nuevo_nombre:
            controlador_categoria.update_categoria(cat_id, nuevo_nombre)
            self.cargar_categorias()
            self.on_update_callback()

    def eliminar_categoria(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Error", "Debe seleccionar una categoría.")
            return

        cat_text = self.lista.get(sel[0])
        cat_id = int(cat_text.split(" - ")[0])
        nombre = cat_text.split(" - ")[1]

        if messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar la categoría '{nombre}'?"):
            try:
                controlador_categoria.delete_categoria(cat_id)
                messagebox.showinfo("Éxito", f"Categoría '{nombre}' eliminada correctamente.")
                self.cargar_categorias()
                self.on_update_callback()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la categoría: {e}")
