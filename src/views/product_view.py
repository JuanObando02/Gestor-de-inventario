import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_producto, controlador_categoria, controlador_movimiento
from src.views.category_view import VentanaCategorias

class VentanaProducto(tk.Toplevel):
    def __init__(self, parent, user, on_complete_callback, producto=None):
        super().__init__(parent)
        self.title("Registrar Producto")
        self.geometry("400x500")
        self.on_complete_callback = on_complete_callback
        self.user = user
        self.producto = producto  # No se usa en esta versión, pero podría ser útil para editar

        fuente = ("Arial", 12)
        # === Código ===
        tk.Label(self, text="Código:").pack(pady=5)
        self.codigo_entry = tk.Entry(self, font=fuente)
        self.codigo_entry.pack()

        # === Nombre ===
        tk.Label(self, text="Nombre:").pack(pady=5)
        self.nombre_entry = tk.Entry(self, font=fuente)
        self.nombre_entry.pack()

        # === Precio ===
        tk.Label(self, text="Precio:").pack(pady=5)
        self.precio_entry = tk.Entry(self, font=fuente)
        self.precio_entry.pack()

        # === Cantidad inicial ===
        tk.Label(self, text="Cantidad inicial:").pack(pady=5)
        self.cantidad_entry = tk.Entry(self, font=fuente)
        self.cantidad_entry.pack()

        # === Descripcion ===
        tk.Label(self, text="Descripcion:").pack(pady=5)
        self.descripcion_entry = tk.Text(self, font=fuente, width=40, height=4)
        self.descripcion_entry.pack()

       # === Categoría ===
        tk.Label(self, text="Categoría:").pack(pady=5)

        frame_cat = tk.Frame(self)
        frame_cat.pack(pady=5)

        self.categorias = controlador_categoria.get_all_categorias()

        # Combobox con nombres de categorías
        self.categoria_cb = ttk.Combobox(
            frame_cat,
            values=[c[1] for c in self.categorias],  # solo nombres
            state="readonly"
        )
        self.categoria_cb.pack(side="left", padx=5)

        # Botón para abrir ventana de categorías
        tk.Button(frame_cat, text="⚙️", command = self.abrir_gestion_categorias).pack(side="left")

        # === Botón Guardar ===
        tk.Button(self, text="Guardar", command=self.guardar_producto).pack(pady=20)

        if self.producto:
            self.precargar_datos()

    def precargar_datos(self):
        self.codigo_entry.insert(0, self.producto["codigo"])
        self.nombre_entry.insert(0, self.producto["nombre"])
        self.precio_entry.insert(0, str(self.producto["precio"]))
        self.descripcion_entry.insert("1.0", self.producto["descripcion"])

        # Bloquear edición de código y cantidad
        self.codigo_entry.config(state="disabled")
        self.cantidad_entry.insert(0, str(self.producto["stock"]))
        self.cantidad_entry.config(state="disabled")
        # Buscar categoría
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
            print(descripcion)

            # Validaciones
            if cantidad_inicial < 0:
                raise ValueError("La cantidad inicial no puede ser negativa.")

            if precio < 0:
                raise ValueError("El precio no puede ser negativo.")
            
            if len(descripcion) > 200:
                raise ValueError("La descripción no puede superar los 200 caracteres.")
            
            # validar categoría seleccionada
            index = self.categoria_cb.current()
            if index == -1:
                messagebox.showerror("Error", "Debe seleccionar una categoría")
                return
            id_categoria = self.categorias[index][0]  # obtiene el id_categoria

            if not codigo or not nombre:
                messagebox.showerror("Error", "Código y Nombre son obligatorios")
                return
            
            if self.producto:  
                # === EDITAR ===
                controlador_producto.update_product(
                    self.producto["id_producto"],
                    self.producto["codigo"],   # usamos el código original
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

            # Refrescar tabla principal
            if self.on_complete_callback:
                self.on_complete_callback()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

        # Captura otros errores
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    def abrir_gestion_categorias(self):
        def refrescar_categorias():
            self.categorias = controlador_categoria.get_all_categorias()
            self.categoria_cb["values"] = [c[1] for c in self.categorias]

        VentanaCategorias(self, refrescar_categorias)