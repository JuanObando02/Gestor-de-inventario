import tkinter as tk
from tkinter import ttk

class SearchFilter(tk.Frame):
    def __init__(self, parent, on_search=None, on_filter=None):
        super().__init__(parent)
        self.search_entry = tk.Entry(self, width=40)
        self.search_entry.pack(side="left", padx=5)

        tk.Button(self, text="Buscar", command=lambda: on_search(self.search_entry.get())).pack(side="left", padx=5)

        # Filtro
        self.filtro = ttk.Combobox(self, values=["Categoría", "Precio", "Stock"])
        self.filtro.set("Filtrar por")
        self.filtro.pack(side="left", padx=5)

        # Botones de ordenar
        tk.Button(self, text="Mayor Stock", command=lambda: on_filter("DESC")).pack(side="left", padx=5)
        tk.Button(self, text="Menor Stock", command=lambda: on_filter("ASC")).pack(side="left", padx=5)

    def get_filtro(self):
        return self.filtro.get()