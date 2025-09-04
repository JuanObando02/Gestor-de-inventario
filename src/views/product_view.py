import tkinter as tk
from tkinter import messagebox
from src.controllers import controlador_producto

class ProductoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Productos")
        self.root.geometry("400x300")

        # Nombre
        tk.Label(root, text="Nombre del producto:").pack(pady=5)
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.pack()

        # Cantidad
        tk.Label(root, text="Cantidad:").pack(pady=5)
        self.entry_cantidad = tk.Entry(root)
        self.entry_cantidad.pack()

        # Precio
        tk.Label(root, text="Precio:").pack(pady=5)
        self.entry_precio = tk.Entry(root)
        self.entry_precio.pack()

        # Botón
        tk.Button(root, text="Agregar Producto", command=self.agregar_producto).pack(pady=10)

    def agregar_producto(self):
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()
        precio = self.entry_precio.get()

        if not nombre or not cantidad or not precio:
            messagebox.showwarning("Campos vacíos", "Debes llenar todos los campos")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
            controlador_producto.agregar_producto(nombre, cantidad, precio)
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente")
            self.entry_nombre.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
            self.entry_precio.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero y precio un número decimal")
