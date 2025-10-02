import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_producto

class ProductTable(tk.Frame):

    def __init__(self, parent, main_view):
        super().__init__(parent, bg="#B6B6B6")
        self.main_view = main_view

        # === Tabla de Productos con Scrollbar ===
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(
            self,
            columns=("codigo", "nombre", "categoria", "descripcion", "precio", "stock", "acciones"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("codigo", text="Código")
        self.tree.column("codigo", width=40, anchor="center")

        self.tree.heading("nombre", text="Nombre")
        self.tree.column("nombre", width=170, anchor="w")

        self.tree.heading("categoria", text="Categoría")
        self.tree.column("categoria", width=80, anchor="center")

        self.tree.heading("descripcion", text="Descripción")
        self.tree.column("descripcion", width=250, anchor="w")

        self.tree.heading("precio", text="Precio")
        self.tree.column("precio", width=30, anchor="e")

        self.tree.heading("stock", text="Stock")
        self.tree.column("stock", width=50, anchor="center")

        self.tree.heading("acciones", text="Acciones")
        self.tree.column("acciones", width=100, anchor="center")

        # Doble click para detectar acciones
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)

        if not item:
            return

        producto = self.tree.item(item, "values")

        if col == "#7":  # la columna "acciones"
            # Aquí decides si es Editar o Eliminar según la posición del click
            x, y, widget = event.x, event.y, event.widget
            bbox = self.tree.bbox(item, col)
            if not bbox:
                return

            click_x = x - bbox[0]
            if click_x < bbox[2] // 2:
                # Buscar el producto en DB
                codigo = producto[0]
                productos = controlador_producto.get_all_products()
                prod = next((p for p in productos if str(p["codigo"]) == str(codigo)), None)

                if prod:
                    from src.views.product_view import VentanaProducto
                    VentanaProducto(self, self.main_view.user, self.main_view.cargar_productos_en_tabla, producto = prod)

            else:
                # Verificar permisos
                if self.main_view.user.role != "admin":
                    messagebox.showerror("Permiso denegado", "Solo los administradores pueden eliminar productos.")
                    print("Rol: ", self.main_view.user)
                    return
                print("Rol: ", self.main_view.user)

                try:
                # Aquí necesitamos el id_producto para borrar
                    codigo = producto[0]
                    # Recuperar producto de DB
                    productos = controlador_producto.get_all_products()
                    prod = next((p for p in productos if str(p["codigo"]) == str(codigo)), None)
                    if not prod:
                        messagebox.showerror("Error", "Producto no encontrado.")
                        return
                    # Confirmación
                    if messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar {prod['nombre']}?"):
                        controlador_producto.delete_product(prod["id_producto"])
                        messagebox.showinfo("Éxito", f"Producto {prod['nombre']} eliminado.")
                        # refrescar tabla
                        self.main_view.cargar_productos_en_tabla()

                except ValueError as e:
                    messagebox.showerror("Error", str(e))