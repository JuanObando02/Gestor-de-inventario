import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_producto, controlador_categoria, controlador_movimiento
from src.views.category_view import VentanaCategorias
from PIL import Image, ImageTk
from src.utils.path_utils import resource_path

class VentanaProducto(tk.Toplevel):
    def __init__(self, parent, user, on_complete_callback, producto=None):
        super().__init__(parent)
        self.title("Registrar Producto")
        self.geometry("450x530")
        self.centrar_ventana(450, 530)
        self.on_complete_callback = on_complete_callback
        self.user = user
        self.producto = producto
        icon_path = resource_path("assets/images/Logo_icon.png")
        self.iconphoto(False, tk.PhotoImage(file=icon_path))

        # Canvas que se expande
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#B6B6B6")
        self.canvas.pack(fill="both", expand=True)

        # Fondo con logo
        try:

            logo_bg_path = resource_path("assets/images/Logo_BG.png")
            self.logo_tk = ImageTk.PhotoImage(Image.open(logo_bg_path).convert("RGBA"))
            self.logo_item = self.canvas.create_image(0, 0, image=self.logo_tk, anchor="center")

        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            self.logo_item = None

        fuente = ("Arial", 12,"bold")

        # === Código ===
        self.text_codigo = self.canvas.create_text(0, 0, text="Código:", fill="black", font = fuente, anchor="w")
        self.codigo_entry = tk.Entry(self, font=fuente)
        self.entry_codigo_item = self.canvas.create_window(0, 0, window=self.codigo_entry)

        # === Nombre ===
        self.text_nombre = self.canvas.create_text(0, 0, text="Nombre:", fill="black", font = fuente, anchor="w")
        self.nombre_entry = tk.Entry(self, font=fuente)
        self.entry_nombre_item = self.canvas.create_window(0, 0, window=self.nombre_entry)

        # === Precio ===
        self.text_precio = self.canvas.create_text(0, 0, text="Precio:", fill="black", font = fuente, anchor="w")
        self.precio_entry = tk.Entry(self, font=fuente)
        self.entry_precio_item = self.canvas.create_window(0, 0, window=self.precio_entry)

        # === Cantidad inicial ===
        self.text_cantidad = self.canvas.create_text(0, 0, text="Cantidad inicial:", fill="black", font=fuente, anchor="w")
        self.cantidad_entry = tk.Entry(self, font=fuente)
        self.entry_cantidad_item = self.canvas.create_window(0, 0, window=self.cantidad_entry)

        # === Descripción ===
        self.text_descripcion = self.canvas.create_text(0, 0, text="Descripción:", fill="black", font=fuente, anchor="w")
        self.descripcion_entry = tk.Text(self, font=fuente, width=40, height=4)
        self.entry_descripcion_item = self.canvas.create_window(0, 0, window=self.descripcion_entry)

        # === Categoría ===
        self.text_categoria = self.canvas.create_text(0, 0, text="Categoría:", fill="black", font=fuente, anchor="w")
        self.categorias = controlador_categoria.get_all_categorias()
        self.categoria_cb = ttk.Combobox(
            self,
            values=[c[1] for c in self.categorias],
            state="readonly"
        )
        
        self.combo_categoria_item = self.canvas.create_window(0, 0, window = self.categoria_cb)
        self.btn_categoria = tk.Button(self, text = "⚙️", command = self.abrir_gestion_categorias)
        self.boton_categoria_item = self.canvas.create_window(0, 0, window = self.btn_categoria)

        # === Botón Guardar ===
        self.guardar_btn = tk.Button(self, text="Guardar", command = self.guardar_producto, bg="#12A617", fg="white", font=("Arial", 12, "bold"))
        self.boton_guardar_item = self.canvas.create_window(0, 0, window = self.guardar_btn)

        if self.producto:
            self.precargar_datos()

        # Reubicar en cada resize
        self.bind("<Configure>", self.reubicar_elementos)

    def reubicar_elementos(self, event=None):
        """Mantener todo centrado al cambiar tamaño de ventana"""
        w = self.winfo_width()
        h = self.winfo_height()
        cx, cy = w // 2, h // 2

        # Logo
        if self.logo_item:
            self.canvas.coords(self.logo_item, cx, cy)

        offset = -200  # desplazamiento vertical inicial
        step = 40      # espacio entre filas

        # Código
        self.canvas.coords(self.text_codigo, cx - 150, cy + offset)
        self.canvas.coords(self.entry_codigo_item, cx + 20, cy + offset)

        # Nombre
        self.canvas.coords(self.text_nombre, cx - 150, cy + offset + step)
        self.canvas.coords(self.entry_nombre_item, cx + 20, cy + offset + step)

        # Precio
        self.canvas.coords(self.text_precio, cx - 150, cy + offset + step * 2)
        self.canvas.coords(self.entry_precio_item, cx + 20, cy + offset + step * 2)

        # Cantidad
        self.canvas.coords(self.text_cantidad, cx - 195, cy + offset + step * 3)
        self.canvas.coords(self.entry_cantidad_item, cx + 20, cy + offset + step * 3)

        # Descripción
        self.canvas.coords(self.text_descripcion, cx - 150, cy + offset + step * 4)
        self.canvas.coords(self.entry_descripcion_item, cx, cy + offset + step * 6)

        # Categoría
        self.canvas.coords(self.text_categoria, cx - 150, cy + offset + step * 8)
        self.canvas.coords(self.combo_categoria_item, cx, cy + offset + step * 8)
        self.canvas.coords(self.boton_categoria_item, cx + 150, cy + offset + step * 8)

        # Botón Guardar
        self.canvas.coords(self.boton_guardar_item, cx, cy + offset + step * 10)

    def centrar_ventana(self, ancho=300, alto=400):
        """Centrar ventana en la pantalla"""
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def precargar_datos(self):
        self.codigo_entry.insert(0, self.producto["codigo"])
        self.nombre_entry.insert(0, self.producto["nombre"])
        self.precio_entry.insert(0, str(self.producto["precio"]))
        self.descripcion_entry.insert("1.0", self.producto["descripcion"])

        self.codigo_entry.config(state="disabled")
        self.cantidad_entry.insert(0, str(self.producto["stock"]))
        self.cantidad_entry.config(state="disabled")

        for idx, c in enumerate(self.categorias):
            if c[0] == self.producto["categoria_id"]:
                self.categoria_cb.current(idx)
                break

    def guardar_producto(self):
        try:
            codigo = self.codigo_entry.get().strip()
            nombre = self.nombre_entry.get().strip()
            precio = float(self.precio_entry.get())
            descripcion = self.descripcion_entry.get("1.0", tk.END).strip()
            cantidad_inicial = int(self.cantidad_entry.get().strip() or 0)

            if cantidad_inicial < 0:
                raise ValueError("La cantidad inicial no puede ser negativa.")
            if precio < 0:
                raise ValueError("El precio no puede ser negativo.")
            if len(descripcion) > 200:
                raise ValueError("La descripción no puede superar los 200 caracteres.")

            index = self.categoria_cb.current()
            if index == -1:
                messagebox.showerror("Error", "Debe seleccionar una categoría")
                return
            id_categoria = self.categorias[index][0]

            if not codigo or not nombre:
                messagebox.showerror("Error", "Código y Nombre son obligatorios")
                return

            if self.producto:
                controlador_producto.update_product(
                    self.producto["id_producto"],
                    self.producto["codigo"],
                    nombre,
                    descripcion,
                    precio,
                    id_categoria
                )
                messagebox.showinfo("Éxito", f"Producto '{nombre}' actualizado correctamente")
            else:
                id_producto = controlador_producto.add_product(
                    codigo=codigo,
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    categoria_id=id_categoria
                )
                if cantidad_inicial > 0:
                    controlador_movimiento.registrar_movimiento(
                        id_producto=id_producto,
                        id_usuario=self.user.id_user,
                        tipo="inicial",
                        cantidad=cantidad_inicial
                    )
                messagebox.showinfo("Éxito", f"Producto '{nombre}' registrado correctamente")

            if self.on_complete_callback:
                self.on_complete_callback()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    def abrir_gestion_categorias(self):
        def refrescar_categorias():
            self.categorias = controlador_categoria.get_all_categorias()
            self.categoria_cb["values"] = [c[1] for c in self.categorias]

        VentanaCategorias(self, refrescar_categorias)
