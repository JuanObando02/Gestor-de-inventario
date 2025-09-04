import tkinter as tk
from tkinter import ttk

class ProductsTable(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        columns = ("Código", "Nombre", "Categoría", "Descripción", "Cantidad", "Precio Unitario")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True)

    def load_data(self, products):
        """Carga lista de productos [(codigo, nombre, ...), (...)]"""
        for row in products:
            self.tree.insert("", "end", values=row)
