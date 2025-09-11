import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_producto
from src.views.components.header_view import Header
from src.views.components.product_table import ProductTable
from src.views.movement_view import VentanaMovimientos
from src.views.product_view import VentanaProducto


class MainApp:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Gestor de Inventario")
        self.root.geometry("900x600")

        # === Encabezado ===
        Header(root, self.registro_producto, self.abrir_movimiento, self.exportar, self.salir)
        tk.Label (root, text=f"Bienvenido", font=("Arial", 24)) .pack(pady=20)

        # === Buscador y Filtros ===

        search_frame = tk.Frame(root)
        search_frame.pack(fill="x", padx=20, pady=5)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Buscar", command = self.buscar).pack(side="left", padx=5)

        filtro = ttk.Combobox(search_frame, values=["Categoría", "Precio", "Stock"])
        filtro.set("Filtrar por")
        filtro.pack(side="left", padx=5)

        tk.Button(search_frame, text="Mayor Stock", command=lambda: self.ordenar("DESC")).pack( side="left", padx=5)
        tk.Button(search_frame, text="Menor Stock", command=lambda: self.ordenar("ASC")).pack(  side="left", padx=5)
        
        # === Tabla de Productos ===
        # Crear tabla de productos
        self.product_table = ProductTable(self.root, self)
        self.product_table.pack(fill = "both", expand=True)
        # Cargar productos
        self.cargar_productos_en_tabla()

    def registro_producto(self):
        VentanaProducto(self.root, self.user, self.cargar_productos_en_tabla)

    def abrir_movimiento(self):
        VentanaMovimientos(self.root, self.user, self.cargar_productos_en_tabla)

    def cargar_productos_en_tabla(self, productos = None):
        """Carga los productos en la tabla. Si no recibe lista de diccionarios, consulta la DB."""
        # limpiar tabla
        for row in self.product_table.tree.get_children():
            self.product_table.tree.delete(row)

        if productos is None:
            #usar controlador para obtener productos
            productos = controlador_producto.get_all_products()

        # insertar filas
        for p in productos:
            self.product_table.tree.insert(
                "", "end",
                values=(p["codigo"], p["nombre"], p["nombre_categoria"], p["descripcion"], p["precio"], p["stock"], "Editar | Eliminar")
            )

    def buscar(self):
        """Filtra productos por lo que escriba el usuario en el search_entry."""
        texto = self.search_entry.get().lower()

        productos = controlador_producto.get_all_products()
        filtrados = [
            p for p in productos
            if texto in p["codigo"].lower()
            or texto in p["nombre"].lower()
            or texto in p["nombre_categoria"].lower()
        ]

        self.cargar_productos_en_tabla(filtrados)

    def ordenar(self, orden="ASC"):
        """Ordena los productos por stock."""
        productos = controlador_producto.get_all_products()
        productos.sort(key=lambda x: x["stock"], reverse=(orden == "DESC"))
        self.cargar_productos_en_tabla(productos)

        messagebox.showinfo("Ordenar", f"Ordenando por stock {orden}")

    def exportar(self):
        messagebox.showinfo("Exportar", "Exportando...")

    def salir(self):
        self.root.quit()
