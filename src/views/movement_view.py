import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_producto, controlador_movimiento
from PIL import Image, ImageTk

class VentanaMovimientos(tk.Toplevel):
    def __init__(self, parent, user, on_complete_callback):
        super().__init__(parent)
        self.title("Registrar Movimiento de Inventario")
        self.geometry("400x350")
        self.user = user
        self.on_complete_callback = on_complete_callback
        self.iconphoto(False, tk.PhotoImage(file="assets/images/Logo_icon.png"))

        # Canvas que se expande
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

        # Widgets
        self.text_producto = self.canvas.create_text(0, 0, text="Producto:", fill="black", font=("Arial", 12, "bold"))
        self.productos = controlador_producto.get_all_products()
        self.producto_cb = ttk.Combobox(
            self,
            values=[f"{p['codigo']} - {p['nombre']}" for p in self.productos],
            state="readonly",
            width=25
        )
        self.combo_producto_item = self.canvas.create_window(0, 0, window=self.producto_cb)

        self.text_tipo = self.canvas.create_text(0, 0, text="Tipo de movimiento:", fill="black", font=("Arial", 12, "bold"))
        self.tipo_cb = ttk.Combobox(self, values=["entrada", "salida"], state="readonly", width=20)
        self.combo_tipo_item = self.canvas.create_window(0, 0, window=self.tipo_cb)

        self.text_cantidad = self.canvas.create_text(0, 0, text="Cantidad:", fill="black", font=("Arial", 12, "bold"))
        self.cantidad_entry = tk.Entry(self, width=10, justify="center", font=("Arial", 14), bg="#FFFFFF")
        self.entry_cantidad_item = self.canvas.create_window(0, 0, window=self.cantidad_entry)

        self.registrar_btn = tk.Button(self, text="Registrar", command=self.registrar, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.boton_item = self.canvas.create_window(0, 0, window=self.registrar_btn)

        # Recolocar elementos al redimensionar
        self.bind("<Configure>", self.reubicar_elementos)

    def reubicar_elementos(self, event=None):
        """Mantener todo centrado al cambiar tamaño de ventana"""
        w = self.winfo_width()
        h = self.winfo_height()

        cx, cy = w // 2, h // 2  # centro de ventana

        # Logo centrado
        if self.logo_item:
            self.canvas.coords(self.logo_item, cx, cy)

        # Producto
        self.canvas.coords(self.text_producto, cx - 120, cy - 80)
        self.canvas.coords(self.combo_producto_item, cx + 40, cy - 80)

        # Tipo de movimiento
        self.canvas.coords(self.text_tipo, cx - 120, cy - 40)
        self.canvas.coords(self.combo_tipo_item, cx + 40, cy - 40)

        # Cantidad
        self.canvas.coords(self.text_cantidad, cx - 120, cy)
        self.canvas.coords(self.entry_cantidad_item, cx + 40, cy)

        # Botón
        self.canvas.coords(self.boton_item, cx, cy + 60)

    def registrar(self):
        try:
            producto_index = self.producto_cb.current()
            if producto_index == -1:
                messagebox.showerror("Error", "Debe seleccionar un producto")
                return

            producto = self.productos[producto_index]
            tipo = self.tipo_cb.get()
            if not tipo:
                messagebox.showerror("Error", "Debe seleccionar tipo de movimiento")
                return

            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return

            controlador_movimiento.registrar_movimiento(
                id_producto=producto['id_producto'],
                id_usuario=self.user.id_user,
                tipo=tipo,
                cantidad=cantidad
            )

            messagebox.showinfo("Éxito", f"{tipo.capitalize()} registrada para {producto['nombre']}")

            if self.on_complete_callback:
                self.on_complete_callback()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
