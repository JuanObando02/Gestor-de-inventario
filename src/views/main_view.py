import tkinter as tk
import csv
from tkinter import ttk, messagebox, filedialog
from src.controllers import controlador_producto
from src.views.components.header_view import Header
from src.views.components.product_table import ProductTable
from src.views.employee_view import VentanaEmpleado, VentanaListaEmpleados
from src.views.movement_view import VentanaMovimientos
from src.views.product_view import VentanaProducto
from src.views.view_csv import VentanaCargaCSV
from src.views.view_csv import VentanaExportar

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

        # estado inicial de orden
        self.orden_actual = "ASC"
        # atributo para guardar el último filtro aplicado
        self.productos_filtrados = None

        # === Encabezado ===
        if self.user.role == "admin":
            Header(root, self.crear_empleado, self.crear_empleado, self.ver_empleados, self.registro_producto, self.abrir_movimiento, self.cerrar_sesion, self.importar_csv, self.exportar_archivo)
        else:
            Header(root, None, None,  None, self.registro_producto, self.abrir_movimiento, self.cerrar_sesion, self.importar_csv, self.exportar_archivo)

        tk.Label (root, text=f"Bienvenido", font=("Arial", 24), bg="#B6B6B6") .pack(pady=20)

        # === Buscador y Filtros ===
        search_frame = tk.Frame(root, bg="#B6B6B6")
        search_frame.pack(pady=10)
        self.search_entry = tk.Entry(search_frame, width=40, bg="#ffffff")
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)

        # Detectar cuando se presiona Enter
        self.search_entry.bind("<Return>", lambda event: self.buscar())
        tk.Button(search_frame, text="Buscar", command = self.buscar, bg="#ffffff").grid(row=0, column=1, padx=5)

        self.filtro = ttk.Combobox(search_frame, values=["Filtrar por","Categoría", "Nombre", "Codigo"])
        self.filtro.set("Filtrar por")
        self.filtro.grid(row=0, column=2, padx=5)

        self.btn_ordenar = tk.Button(search_frame, text="Mayor Stock", command=self.toggle_orden, bg="#ffffff")
        self.btn_ordenar.grid(row=0, column=3, padx=5)
        
        for i in range(5):
            search_frame.grid_columnconfigure(i, weight=1)

        # === Tabla de Productos ===
        table_container = tk.Frame(self.root)
        table_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.product_table = ProductTable(table_container, self)
        self.product_table.pack(fill="both", expand=True)
        self.valor_inventario_label = tk.Label(
            self.root, 
            text="Valor Total del Inventario: $0.00",
            font=("Arial", 14, "bold"),
            bg="#B6B6B6",  # Mismo color de fondo
            fg="#333333"   # Color de texto oscuro para contraste
        )

        self.valor_inventario_label.pack(pady=(0, 10)) # Padding abajo
        # Cargar productos
        self.cargar_productos_en_tabla()

    def toggle_orden(self):
        """Alterna entre ASC y DESC al ordenar."""
        if self.orden_actual == "ASC":
            self.ordenar("DESC")
            self.orden_actual = "DESC"
            self.btn_ordenar.config(text="Menor Stock")
        else:
            self.ordenar("ASC")
            self.orden_actual = "ASC"
            self.btn_ordenar.config(text="Mayor Stock")

    def centrar_ventana(self, ancho=300, alto=400):
        """Centrar ventana en la pantalla"""
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_empleado(self):
        VentanaEmpleado(self.root)

    def ver_empleados(self):
        VentanaListaEmpleados(self.root, self.user)

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
        # actualizar la lista actual en memoria
        self.productos_filtrados = productos
        self.calcular_y_actualizar_valor_inventario()

    def buscar(self):
        """Filtra productos por lo que escriba el usuario en el search_entry."""
        texto = self.search_entry.get().lower()
        filtro = self.filtro.get()

        productos = controlador_producto.get_all_products()

        if filtro == "Categoría":
                filtrados = [p for p in productos if texto in p["nombre_categoria"].lower()]
        elif filtro == "Nombre":
                filtrados = [p for p in productos if texto in str(p["nombre"]).lower()]
        elif filtro == "Codigo":
                filtrados = [p for p in productos if texto in str(p["codigo"]).lower()]
        else:  # búsqueda general si no hay filtro seleccionado
            filtrados = [
                p for p in productos
                if texto in p["codigo"].lower()
                or texto in p["nombre"].lower()
                or texto in p["nombre_categoria"].lower()
            ]

        self.cargar_productos_en_tabla(filtrados)

    def ordenar(self, orden="ASC"):
        """Ordena los productos por stock respetando el último filtro aplicado."""
        productos = self.productos_filtrados or controlador_producto.get_all_products()
        productos.sort(key=lambda x: x["stock"], reverse=(orden == "DESC"))
        self.cargar_productos_en_tabla(productos)

    def importar_csv(self):
        """Abrir ventana para importar CSV"""
        VentanaCargaCSV(self.root, self)
    
    def exportar_archivo(self):
        VentanaExportar(self.root, self)

    def cerrar_sesion(self):
        """Cerrar sesión y volver a la pantalla de login."""
        self.root.destroy()  # cerrar ventana principal

        import tkinter as tk
        from src.views.login_view import LoginApp  

        nueva_root = tk.Tk()
        LoginApp(nueva_root)  # volver a la ventana de login
        nueva_root.mainloop()

    def calcular_y_actualizar_valor_inventario(self):
        try:
            #obtener todos los productos
            #productos = controlador_producto.get_all_products()
            valor_total = 0.0
            #bucar sobre los productos filtrados
            for producto in self.productos_filtrados:
                precio = float(producto.get("precio", 0))
                stock = int(producto.get("stock", 0))
                valor_total += precio * stock
                
            texto_formateado = f"${valor_total:,.2f}"
            
            self.valor_inventario_label.config(text=f"Valor Total del Inventario: {texto_formateado}")

        except Exception as e:
            
            print(f"Error al calcular el valor del inventario: {e}")
            self.valor_inventario_label.config(text="Valor Total del Inventario: Error de cálculo")