import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_producto
from src.views.components.header_view import Header
from src.views.components.product_table import ProductTable
from src.views.employee_view import VentanaEmpleado
from src.views.movement_view import VentanaMovimientos
from src.views.product_view import VentanaProducto


class MainApp:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Gestor de Inventario")
        self.root.geometry("900x600")
        self.centrar_ventana(900, 600)
        self.root.configure(bg="#B6B6B6")
        self.root.iconphoto(False, tk.PhotoImage(file="assets/images/Logo_icon.png"))
        print("Página Principal")

        # === Encabezado ===
        if self.user.role == "admin":
            Header(root, self.crear_empleado, self.registro_producto, self.abrir_movimiento, self.exportar, self.cerrar_sesion)
        else:
            Header(root, None, self.registro_producto, self.abrir_movimiento, self.exportar, self.cerrar_sesion)

        tk.Label (root, text=f"Bienvenido", font=("Arial", 24), bg="#B6B6B6") .pack(pady=20)

        # === Buscador y Filtros ===

        search_frame = tk.Frame(root, bg="#B6B6B6")
        search_frame.pack(pady=10)

        self.search_entry = tk.Entry(search_frame, width=40, bg="#ffffff")
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)
        tk.Button(search_frame, text="Buscar", command = self.buscar, bg="#ffffff").grid(row=0, column=1, padx=5)

        filtro = ttk.Combobox(search_frame, values=["Categoría", "Precio", "Stock"])
        filtro.set("Filtrar por")
        filtro.grid(row=0, column=2, padx=5)

        tk.Button(search_frame, text="Mayor Stock", command=lambda: self.ordenar("DESC"), bg="#ffffff").grid(row=0, column=3, padx=5)
        tk.Button(search_frame, text="Menor Stock", command=lambda: self.ordenar("ASC"), bg="#ffffff").grid(row=0, column=4, padx=5)
        
        for i in range(5):
            search_frame.grid_columnconfigure(i, weight=1)


        # === Tabla de Productos ===
        # Crear tabla de productos
        self.product_table = ProductTable(self.root, self)
        self.product_table.pack(fill = "both", expand=True)
        # Cargar productos
        self.cargar_productos_en_tabla()

    def centrar_ventana(self, ancho=300, alto=400):
        """Centrar ventana en la pantalla"""
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_empleado(self):
        VentanaEmpleado(self.root)

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

    def cerrar_sesion(self):
        """Cerrar sesión y volver a la pantalla de login."""
        self.root.destroy()  # cerrar ventana principal

        import tkinter as tk
        from src.views.login_view import LoginApp  

        nueva_root = tk.Tk()
        LoginApp(nueva_root)  # volver a la ventana de login
        nueva_root.mainloop()
