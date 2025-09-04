import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_producto
from src.views.components.header_view import Header
from src.views.components.search_view import SearchFilter

class MainApp:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Gestor de Inventario")
        self.root.geometry("900x600")

        # === Encabezado ===
        Header(root, self.registro, self.exportar, self.salir)
        tk.Label (root, text=f"Bienvenido", font=("Arial", 24)) .pack(pady=20)

        # === Buscador y Filtros ===
        #SearchFilter(self, on_search=self.search_products, on_filter=self.filter_products).pack(fill="x", pady=5)

        search_frame = tk.Frame(root)
        search_frame.pack(fill="x", padx=20, pady=5)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Buscar", command=self.buscar).pack(side="left", padx=5)

        filtro = ttk.Combobox(search_frame, values=["Categoría", "Precio", "Stock"])
        filtro.set("Filtrar por")
        filtro.pack(side="left", padx=5)

        tk.Button(search_frame, text="Mayor Stock", command=lambda: self.ordenar("DESC")).pack(side="left", padx=5)
        tk.Button(search_frame, text="Menor Stock", command=lambda: self.ordenar("ASC")).pack(side="left", padx=5)

        # === Tabla de Productos ===
        self.tree = ttk.Treeview(root, columns=("codigo", "nombre", "categoria", "descripcion", "cantidad", "precio"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        for col in ("codigo", "nombre", "categoria", "descripcion", "cantidad", "precio"):
            self.tree.heading(col, text=col.capitalize())

        self.cargar_productos()

        # === Total ===
        self.lbl_total = tk.Label(root, text="Total: $0", font=("Arial", 14))
        self.lbl_total.pack(pady=10)

    # === Funciones ===
    def cargar_productos(self):
        messagebox.showinfo("Cargar")

    def buscar(self):
        messagebox.showinfo("Buscar", f"Buscando: {self.search_entry.get()}")


    def ordenar(self, orden):
        messagebox.showinfo("Ordenar", f"Ordenando por stock {orden}")

    def registro(self):
        messagebox.showinfo("Registro", "Abrir formulario de registro")

    def exportar(self):
        messagebox.showinfo("Exportar", "Exportando...")

    def salir(self):
        self.root.quit()

    def search_products(self, query):
        print("Buscar:", query)

    def filter_products(self, filter_option):
        print("Filtro:", filter_option)