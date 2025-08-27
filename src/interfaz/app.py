import tkinter as tk
from tkinter import ttk, messagebox
from modelos import Producto
from persistencia import Persistencia


class App:
    def __init__(self, root, rol):
        self.root = root
        self.root.title("Gestor de Inventario")
        self.root.geometry("700x400")
        self.rol = rol  # Guardamos el rol del usuario

        self.persistencia = Persistencia()
        self.inventario = self.persistencia.cargar()

        # Frame entradas
        frame_inputs = tk.Frame(self.root)
        frame_inputs.pack(pady=10)

        tk.Label(frame_inputs, text="Código").grid(row=0, column=0)
        tk.Label(frame_inputs, text="Nombre").grid(row=0, column=1)
        tk.Label(frame_inputs, text="Descripción").grid(row=0, column=2)
        tk.Label(frame_inputs, text="Cantidad").grid(row=0, column=3)
        tk.Label(frame_inputs, text="Precio").grid(row=0, column=4)

        self.entry_codigo = tk.Entry(frame_inputs, width=10)
        self.entry_nombre = tk.Entry(frame_inputs, width=15)
        self.entry_descripcion = tk.Entry(frame_inputs, width=15)
        self.entry_cantidad = tk.Entry(frame_inputs, width=7)
        self.entry_precio = tk.Entry(frame_inputs, width=7)

        self.entry_codigo.grid(row=1, column=0)
        self.entry_nombre.grid(row=1, column=1)
        self.entry_descripcion.grid(row=1, column=2)
        self.entry_cantidad.grid(row=1, column=3)
        self.entry_precio.grid(row=1, column=4)

        tk.Button(frame_inputs, text="Agregar", command=self.agregar_producto).grid(row=1, column=5, padx=10)

        # Tabla
        self.tree = ttk.Treeview(self.root, columns=("codigo", "nombre", "descripcion", "cantidad", "precio", "total"), show="headings")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("total", text="Valor Total")
        self.tree.pack(expand=True, fill="both")

        # Botones inferiores
        if self.rol == "admin":
            tk.Button(self.root, text="Eliminar", command=self.eliminar_producto).pack(side="left", padx=10, pady=5)
        else:
            tk.Button(self.root, text="Eliminar (no permitido)", state="disabled").pack(side="left", padx=10, pady=5)

        tk.Button(self.root, text="Guardar", command=self.guardar).pack(side="left", padx=10, pady=5)

        self.mostrar_inventario()

    def agregar_producto(self):
        try:
            p = Producto(
                self.entry_codigo.get(),
                self.entry_nombre.get(),
                self.entry_descripcion.get(),
                int(self.entry_cantidad.get()),
                float(self.entry_precio.get())
            )
            self.inventario.agregar_producto(p)
            self.mostrar_inventario()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_producto(self):
        if self.rol != "admin":
            messagebox.showwarning("Permiso denegado", "Solo el administrador puede eliminar productos.")
            return
        selected = self.tree.selection()
        if not selected:
            return
        codigo = self.tree.item(selected[0], "values")[0]
        self.inventario.eliminar_producto(codigo)
        self.mostrar_inventario()

    def guardar(self):
        self.persistencia.guardar(self.inventario)
        messagebox.showinfo("Éxito", "Inventario guardado.")

    def mostrar_inventario(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.inventario.productos:
            self.tree.insert("", "end", values=(
                p.codigo, p.nombre, p.descripcion, p.cantidad, p.precio_unitario, p.calcular_valor_total()
            ))
