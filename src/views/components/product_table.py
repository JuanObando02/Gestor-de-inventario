from tkinter import ttk

class ProductTable(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # === Tabla de Productos ===
        self.tree = ttk.Treeview(
            self,
            columns=("codigo", "nombre", "categoria", "descripcion", "precio", "stock"),
            show="headings"
        )
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Definir encabezados y columnas con ancho
        self.tree.heading("codigo", text="Código")
        self.tree.column("codigo", width=40, anchor="center")

        self.tree.heading("nombre", text="Nombre")
        self.tree.column("nombre", width=120, anchor="w")

        self.tree.heading("categoria", text="Categoría")
        self.tree.column("categoria", width=50, anchor="center")

        self.tree.heading("descripcion", text="Descripción")
        self.tree.column("descripcion", width=200, anchor="w")

        self.tree.heading("precio", text="Precio")
        self.tree.column("precio", width=100, anchor="e")

        self.tree.heading("stock", text="Stock")
        self.tree.column("stock", width=80, anchor="center")

    def cargar_productos(self, productos):
        # Limpia antes de cargar
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Inserta los productos
        for p in productos:
            self.tree.insert(
                "",
                "end",
                values=(p["codigo"],p["nombre"],p["nombre_categoria"], p["descripcion"],p["precio"],p["stock"]
                )
            )
