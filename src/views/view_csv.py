import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv

class VentanaCargaCSV(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Importar CSV")
        self.geometry("700x400")
        self.configure(bg="#EAEAEA")

        tk.Label(self, text="Importar productos desde CSV", font=("Arial", 14), bg="#EAEAEA").pack(pady=10)

        # Botón para seleccionar archivo
        tk.Button(self, text="Seleccionar archivo CSV", command=self.cargar_csv).pack(pady=5)

        # Frame de tabla
        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear tabla
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("codigo", "nombre", "categoria", "descripcion", "precio", "stock"),
            show="headings"
        )

        # Encabezados
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")

        # Ajustar tamaños
        self.tree.column("codigo", width=80)
        self.tree.column("nombre", width=120)
        self.tree.column("categoria", width=100)
        self.tree.column("descripcion", width=180)
        self.tree.column("precio", width=80)
        self.tree.column("stock", width=60)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    def cargar_csv(self):
        """Abrir explorador de archivos y cargar datos en la tabla"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, newline='', encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                # limpiar la tabla antes de insertar
                for row in self.tree.get_children():
                    self.tree.delete(row)

                for row in reader:
                    self.tree.insert("", "end", values=(
                        row.get("codigo", ""),
                        row.get("nombre", ""),
                        row.get("nombre_categoria", ""),
                        row.get("descripcion", ""),
                        row.get("precio", ""),
                        row.get("stock", "")
                    ))

            messagebox.showinfo("Éxito", "Archivo cargado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
