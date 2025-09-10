from tkinter import ttk, messagebox

class ProductTable(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

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
                messagebox.showinfo("Editar", f"Editar producto: {producto[1]}")
            else:
                messagebox.showinfo("Eliminar", f"Eliminar producto: {producto[1]}")