from tkinter import ttk, messagebox
from src.controllers import controlador_producto

class ProductTable(ttk.Frame):
    def __init__(self, parent, main_view):
        super().__init__(parent)
        self.main_view = main_view 

        # === Tabla de Productos ===
        self.tree = ttk.Treeview(
            self,
            columns=("codigo", "nombre", "categoria", "descripcion", "precio", "stock", "acciones"),
            show="headings"
        )
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Definir encabezados y columnas con ancho
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

        # Nueva columna de acciones
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
        
        # Columna de acciones

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
                    print("self.main_view.user:", self.main_view.user)
                    return
                print("self.main_view.user:", self.main_view.user)

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