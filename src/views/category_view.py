import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.controllers import controlador_categoria

# === Ventana para gestionar categorías ===
class VentanaCategorias(tk.Toplevel):
    def __init__(self, parent, on_update_callback):
        super().__init__(parent, bg="#B6B6B6")
        self.title("Gestionar Categorías")
        self.geometry("300x300")
        self.on_update_callback = on_update_callback

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_categorias()

        tk.Button(self, text="Agregar", bg="#ffffff", command=self.agregar_categoria).pack(pady=5)
        tk.Button(self, text="Editar", bg="#ffffff", command=self.editar_categoria).pack(pady=5)
        tk.Button(self, text="Eliminar", bg="#210ed1", command=self.eliminar_categoria).pack(pady=5)

    def cargar_categorias(self):
        self.lista.delete(0, tk.END)
        categorias = controlador_categoria.get_all_categorias()
        for c in categorias:
            self.lista.insert(tk.END, f"{c[0]} - {c[1]}")

    def agregar_categoria(self):
        nombre = simpledialog.askstring("Nueva categoría", "Ingrese el nombre:")
        if nombre:
            controlador_categoria.add_categoria(nombre)
            self.cargar_categorias()
            self.on_update_callback()

    def editar_categoria(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una categoría.")
            return
        cat_text = self.lista.get(sel[0])
        cat_id = int(cat_text.split(" - ")[0])
        nuevo_nombre = simpledialog.askstring("Editar categoría", "Nuevo nombre:")
        if nuevo_nombre:
            controlador_categoria.update_categoria(cat_id, nuevo_nombre)
            self.cargar_categorias()
            self.on_update_callback()

    def eliminar_categoria(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Error", "Debe seleccionar una categoría.")
            return

        cat_text = self.lista.get(sel[0])
        cat_id = int(cat_text.split(" - ")[0])
        nombre = cat_text.split(" - ")[1]

        if messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar la categoría '{nombre}'?"):
            try:
                controlador_categoria.delete_categoria(cat_id)
                messagebox.showinfo("Éxito", f"Categoría '{nombre}' eliminada correctamente.")
                self.cargar_categorias()  # refrescar lista
                self.on_update_callback()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la categoría: {e}")
