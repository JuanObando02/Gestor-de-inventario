import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import csv
import openpyxl
import sqlite3
import os
from src.controllers import controlador_producto, controlador_movimiento
from itertools import zip_longest

DB_PATH = os.path.join("data", "inventario.db")

class VentanaCargaCSV(tk.Toplevel):
    """
    Ventana para cargar un CSV de productos e importarlos usando los controladores
    existentes (controlador_producto.add_product y controlador_movimientos.registrar_movimiento).
    """

    def __init__(self, master, main_app=None):
        """
        master: widget padre (normalmente root)
        main_app: instancia de MainApp (opcional). Si se pasa se usa main_app.user para id_usuario.
        """
        super().__init__(master)
        self.main_app = main_app  # puede ser None; en MainApp pasar self
        self.title("Importar CSV")
        self.geometry("800x500")
        self.centrar_ventana(700, 500)
        self.configure(bg="#B6B6B6")
        self.iconphoto(False, tk.PhotoImage(file="assets/images/Logo_icon.png"))

        tk.Label(self, text="Importar Productos desde CSV", font=("Arial", 16, "bold"), bg="#B6B6B6").pack(pady=10)

        btn_frame = tk.Frame(self, bg="#B6B6B6")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Seleccionar archivo CSV", command=self.cargar_csv).grid(row=0, column=0, padx=5)

        # botón import es accesible más tarde (se guarda en self)
        self.btn_import = tk.Button(btn_frame, text="Importar a la base de datos", command=self.importar_a_db)
        self.btn_import.grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="Limpiar tabla", command=self.limpiar_tabla).grid(row=0, column=2, padx=5)

        # NUEVO: botón para eliminar filas marcadas como error
        self.btn_eliminar_errores = tk.Button(btn_frame, text="Eliminar filas con errores", command=self.eliminar_filas_error)
        self.btn_eliminar_errores.grid(row=0, column=3, padx=5)

        # Inicialmente desactivamos import hasta que se cargue algo
        self.btn_import.config(state="disabled")

        # ---------- Mensaje de contexto encima de la tabla ----------
        self.info_frame = tk.Frame(self, bg="#357BB7", bd=1, relief="solid", padx=8, pady=6)
        self.info_frame.pack(fill="x", padx=10, pady=(8, 6))

        info_text = (
            "Formato CSV aceptado:\n"
            "- Cabeceras recomendadas (cualquiera de estas variantes):\n"
            "  codigo, nombre, nombre_categoria, descripcion, precio, stock\n"
            "  (también se aceptan: code, name, categoria, description, price, cantidad)\n"
            "- Separador: se detectan automáticamente ',', ';', tab o '|'.\n"
            "- Precio: puede usar punto o coma decimal (ej: 1200.50 o 1200,50). Miles con '.' serán manejados.\n"
            "- Stock: entero (si está vacío se toma 0).\n"
            "- Campos obligatorios: 'codigo' y 'nombre'.\n"
            "- Categorías no encontradas se asignan a 'Otros' (id = 10).\n"
            "- Filas vacías o mal formateadas se marcarán en rojo y bloquearán la importación.\n"
        )

        lbl_info = tk.Label(self.info_frame, text=info_text, justify="left", anchor="w", font=("Arial", 10), fg="white", bg="#357BB7")
        lbl_info.pack(side="left", fill="x", expand=True)

        btn_right_frame = tk.Frame(self.info_frame, bg="#357BB7")
        btn_right_frame.pack(side="right", anchor="n")

        # Botón para ver un ejemplo y poder guardarlo
        btn_ejemplo = tk.Button(btn_right_frame, text="Ejemplo CSV", command=self.mostrar_ejemplo)
        btn_ejemplo.pack(padx=4, pady=2, anchor="ne")

        # Ocultar el mensaje de ayuda
        btn_ocultar = tk.Button(btn_right_frame, text="Ocultar", command=lambda: self.info_frame.pack_forget())
        btn_ocultar.pack(padx=4, pady=2, anchor="ne")

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("codigo", "nombre", "categoria", "descripcion", "precio", "stock"),
            show="headings",
            selectmode="extended"
        )
        self.tree.tag_configure('error', background='#FFD6D6')  # filas con error en rojo claro

        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")

        self.tree.column("codigo", width=100)
        self.tree.column("nombre", width=180)
        self.tree.column("categoria", width=140)
        self.tree.column("descripcion", width=220)
        self.tree.column("precio", width=80)
        self.tree.column("stock", width=60)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.current_file = None

        self.transient(master)
        self.grab_set()
        self.focus()
        
    def centrar_ventana(self, ancho=300, alto=400):
        """Centrar ventana en la pantalla"""
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def limpiar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.actualizar_estado_importar()

    def detectar_delimitador(self, file_path, enc="utf-8"):
        import csv
        sample = ""
        try:
            with open(file_path, "r", encoding=enc, errors="replace") as f:
                for _ in range(20):
                    line = f.readline()
                    if not line:
                        break
                    sample += line
        except Exception:
            return ","
        try:
            sniff = csv.Sniffer()
            dialect = sniff.sniff(sample, delimiters=[",", ";", "\t", "|"])
            return dialect.delimiter
        except Exception:
            if ";" in sample and sample.count(";") > sample.count(","):
                return ";"
            if "\t" in sample:
                return "\t"
            if "|" in sample:
                return "|"
            return ","

    def cargar_csv(self):
        import csv
        from itertools import zip_longest
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if not file_path:
            return

        # limpiar la tabla
        self.limpiar_tabla()

        delimiter = self.detectar_delimitador(file_path)

        errores = []  # lista de tuplas (numero_linea, mensaje)
        fila_index = 0
        headers = None

        try:
            with open(file_path, newline='', encoding="utf-8", errors="replace") as csvfile:
                reader = csv.reader(csvfile, delimiter=delimiter)
                try:
                    first = next(reader)
                    fila_index += 1
                except StopIteration:
                    messagebox.showwarning("Archivo vacío", "El archivo CSV está vacío.")
                    return

                header_lower = [c.strip().lower() for c in first]
                has_header = any(h in header_lower for h in ("codigo", "code", "nombre", "name", "precio", "price"))
                if has_header:
                    headers = [h.strip() for h in first]
                    iterator = reader
                else:
                    headers = [f"col{i}" for i in range(1, len(first)+1)]
                    iterator = [first] + list(reader)

                for raw in iterator:
                    fila_index += 1
                    # saltar filas completamente vacías
                    if all((not cell) or (str(cell).strip() == "") for cell in raw):
                        continue

                    # normalizar row -> dict con headers
                    row_dict = {headers[i]: (raw[i].strip() if i < len(raw) else "") for i in range(len(headers))}

                    # extracción flexible de campos
                    codigo = (row_dict.get("codigo") or row_dict.get("code") or row_dict.get("col1") or "").strip()
                    nombre = (row_dict.get("nombre") or row_dict.get("name") or row_dict.get("col2") or "").strip()
                    nombre_categoria = (row_dict.get("nombre_categoria") or row_dict.get("categoria") or row_dict.get("category") or "").strip()
                    descripcion = (row_dict.get("descripcion") or row_dict.get("description") or "").strip()

                    # precio: tolera coma decimal y miles con punto
                    precio_raw = (row_dict.get("precio") or row_dict.get("price") or "").strip()
                    precio_val = ""
                    if precio_raw != "":
                        try:
                            precio_val = float(precio_raw.replace(".", "").replace(",", "."))
                        except Exception:
                            errores.append((fila_index, f"Precio inválido: '{precio_raw}'"))

                    # stock opcional
                    stock_raw = (row_dict.get("stock") or row_dict.get("cantidad") or "").strip()
                    stock_val = ""
                    if stock_raw != "":
                        try:
                            stock_val = int(float(stock_raw.replace(",", ".")))
                        except Exception:
                            errores.append((fila_index, f"Stock inválido: '{stock_raw}'"))

                    # validaciones mínimas
                    fila_tiene_error = False
                    motivo = []
                    if not codigo:
                        motivo.append("Código vacío")
                        fila_tiene_error = True
                    if not nombre:
                        motivo.append("Nombre vacío")
                        fila_tiene_error = True

                    # verificar si errores acumulados para esta fila
                    mensajes_fila = [m for f, m in errores if f == fila_index]
                    if mensajes_fila:
                        fila_tiene_error = True
                        motivo.extend(mensajes_fila)

                    vals = (codigo, nombre, nombre_categoria, descripcion, precio_val if precio_val != "" else "", stock_val)
                    # insertar en vista; si hay error marcar con tag 'error'
                    if fila_tiene_error:
                        self.tree.insert("", "end", values=vals, tags=('error',))
                    else:
                        self.tree.insert("", "end", values=vals)

            # si hubo errores, mostrar resumen y ofrecer exportarlos
            errores_por_fila = {}
            for f, m in errores:
                errores_por_fila.setdefault(f, []).append(m)
            if errores_por_fila:
                resumen = f"Se detectaron {len(errores_por_fila)} fila(s) con problemas.\n" \
                        "La importación NO podrá realizarse hasta corregirlas.\n" \
                        "¿Deseas exportar las filas con problemas para revisarlas?"
                if messagebox.askyesno("Errores en CSV", resumen):
                    # llamar a exportar_errores_csv (función incluida abajo)
                    self.exportar_errores_csv(file_path, [(k, "; ".join(v)) for k, v in errores_por_fila.items()], delimiter)
                messagebox.showinfo("Revisión requerida", "Corrige las filas señaladas en rojo antes de intentar importar.")
            else:
                messagebox.showinfo("Carga OK", "Archivo cargado correctamente. Puedes proceder a importar.")

            self.current_file = file_path

        except Exception as e:
            messagebox.showerror("Error lectura CSV", f"Ocurrió un error al leer el CSV:\n{e}")
        self.actualizar_estado_importar()

    def _obtener_user_id(self):
        """Intenta obtener id de usuario desde main_app.user; si no, fallback a 1."""
        if self.main_app:
            user = getattr(self.main_app, "user", None)
            # el objeto user en tu proyecto parece tener .id o .id_usuario o .role; intentamos varias formas
            if isinstance(user, dict):
                for key in ("id_usuario", "id", "user_id"):
                    if key in user:
                        return int(user[key])
            else:
                for attr in ("id_usuario", "id", "user_id"):
                    if hasattr(user, attr):
                        try:
                            return int(getattr(user, attr))
                        except Exception:
                            pass
        # fallback
        return 1

    def _categoria_to_id(self, nombre_cat, db_conn):
        """
        Si la categoria existe devuelve su id;
        si no existe intenta usar/crear 'Otros' con id = 10; si falla crea 'Otros' con id autoincrement.
        """
        nombre_cat = (nombre_cat or "").strip()
        cur = db_conn.cursor()

        if nombre_cat:
            cur.execute("SELECT id_categoria FROM Categorias WHERE nombre = ?", (nombre_cat,))
            r = cur.fetchone()
            if r:
                return r[0]

        # intentar id 10
        cur.execute("SELECT id_categoria FROM Categorias WHERE id_categoria = 10")
        r = cur.fetchone()
        if r:
            return 10

        # insertar id 10 si es posible
        try:
            cur.execute("INSERT INTO Categorias (id_categoria, nombre) VALUES (?, ?)", (10, "Otros"))
            db_conn.commit()
            return 10
        except Exception:
            # si falla, buscar por nombre 'Otros'
            cur.execute("SELECT id_categoria FROM Categorias WHERE nombre = ?", ("Otros",))
            r2 = cur.fetchone()
            if r2:
                return r2[0]
            cur.execute("INSERT INTO Categorias (nombre) VALUES (?)", ("Otros",))
            db_conn.commit()
            return cur.lastrowid

    def exportar_errores_csv(self, origen_path, errores, delimiter=","):
        """ errores: lista de tuplas (numero_linea, motivo_str) """
        import csv
        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile="errores_csv.csv",
            title="Guardar errores como..."
        )
        if not save_path:
            return
        try:
            with open(origen_path, newline='', encoding="utf-8", errors="replace") as f_in:
                reader = list(csv.reader(f_in, delimiter=delimiter))
            filas_indices = {e[0] for e in errores}
            motivos_por_linea = {e[0]: e[1] for e in errores}
            with open(save_path, "w", newline='', encoding="utf-8") as f_out:
                writer = csv.writer(f_out)
                writer.writerow(["numero_linea", "motivo", "contenido_linea"])
                for idx, line in enumerate(reader, start=1):
                    if idx in filas_indices:
                        writer.writerow([idx, motivos_por_linea.get(idx, ""), delimiter.join(line)])
            messagebox.showinfo("Exportado", f"Errores guardados en: {save_path}")
        except Exception as e:
            messagebox.showerror("Error exportar", f"No se pudo exportar errores:\n{e}")

    def contar_filas_error(self):
        """Devuelve la cantidad de filas en la vista que tienen el tag 'error'."""
        cuenta = 0
        for iid in self.tree.get_children():
            tags = self.tree.item(iid).get("tags", [])
            if 'error' in tags:
                cuenta += 1
        return cuenta

    def actualizar_estado_importar(self):
        """
        Habilita o deshabilita el botón de importar según si hay filas y si existen errores.
        - Si no hay filas -> deshabilita.
        - Si hay filas y NO hay errores -> habilita.
        - Si hay errores -> deshabilita (bloqueo).
        """
        total_filas = len(self.tree.get_children())
        errores = self.contar_filas_error()

        if total_filas == 0:
            self.btn_import.config(state="disabled")
        else:
            # si hay errores, bloqueamos import
            if errores > 0:
                self.btn_import.config(state="disabled")
            else:
                self.btn_import.config(state="normal")

    def eliminar_filas_error(self):
        """
        Elimina todas las filas marcadas con el tag 'error' de la vista.
        Actualiza el estado del botón importar.
        """
        # recolectar iids para evitar modificar el tree mientras iteramos
        iids_a_borrar = [iid for iid in self.tree.get_children() if 'error' in self.tree.item(iid).get("tags", [])]
        if not iids_a_borrar:
            messagebox.showinfo("Eliminar errores", "No hay filas con error para eliminar.")
            return

        # confirmar acción con el usuario
        if not messagebox.askyesno("Confirmar eliminación", f"Se eliminarán {len(iids_a_borrar)} fila(s) con errores. ¿Deseas continuar?"):
            return

        for iid in iids_a_borrar:
            self.tree.delete(iid)

        messagebox.showinfo("Eliminado", f"Se eliminaron {len(iids_a_borrar)} fila(s) con error.")
        # actualizar estado del botón importar y cualquier otra UI necesaria
        self.actualizar_estado_importar()

    def importar_a_db(self):
        """
        Importa a la base de datos todas las filas válidas que estén en la tabla (sin tag 'error').
        Usa controlador_producto.add_product y controlador_movimiento.registrar_movimiento.
        """
        # 1) bloquear si hay filas con tag 'error'
        filas_error = []
        for iid in self.tree.get_children():
            tags = self.tree.item(iid).get("tags", [])
            if 'error' in tags:
                vals = self.tree.item(iid)["values"]
                filas_error.append((iid, vals))

        if filas_error:
            ejemplos = "\n".join([f"{v[0]} - {v[1]}" for _, v in filas_error[:6]])
            mensaje = (f"Hay {len(filas_error)} fila(s) con errores. La importación está BLOQUEADA hasta corregirlas.\n\n"
                    f"Ejemplos:\n{ejemplos}\n\n¿Deseas exportar las filas con errores para revisarlas?")
            if messagebox.askyesno("Importación bloqueada", mensaje):
                # Exportar filas con errores desde la vista
                save_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                        filetypes=[("CSV", "*.csv")],
                                                        initialfile="errores_vista.csv")
                if save_path:
                    try:
                        import csv
                        with open(save_path, "w", newline="", encoding="utf-8") as f_out:
                            writer = csv.writer(f_out)
                            writer.writerow(["codigo","nombre","categoria","descripcion","precio","stock","motivo"])
                            for iid, vals in filas_error:
                                codigo = vals[0] if len(vals)>0 else ""
                                nombre = vals[1] if len(vals)>1 else ""
                                categoria = vals[2] if len(vals)>2 else ""
                                descripcion = vals[3] if len(vals)>3 else ""
                                precio = vals[4] if len(vals)>4 else ""
                                stock = vals[5] if len(vals)>5 else ""
                                writer.writerow([codigo,nombre,categoria,descripcion,precio,stock,"Fila con datos inválidos o faltantes"])
                        messagebox.showinfo("Exportado", f"Filas con errores exportadas a: {save_path}")

                    except Exception as e:
                        messagebox.showerror("Error exportar", f"No se pudo exportar:\n{e}")
            return  # bloqueamos la importación

        # 2) construir lista de productos desde la vista (solo filas sin tag 'error')
        productos = []
        for iid in self.tree.get_children():
            tags = self.tree.item(iid).get("tags", [])
            if 'error' in tags:
                continue
            vals = self.tree.item(iid)["values"]
            # normalizar/parsear precio y stock
            precio = vals[4] if len(vals) > 4 else ""
            stock = vals[5] if len(vals) > 5 else 0
            # intentar parsear si viene como texto
            try:
                if precio in (None, "", "None"):
                    precio_val = 0.0
                elif isinstance(precio, (int, float)):
                    precio_val = float(precio)
                else:
                    # admitir formatos con coma decimal y separadores de miles
                    precio_val = float(str(precio).replace(".", "").replace(",", "."))
            except Exception:
                precio_val = 0.0

            try:
                if stock in (None, "", "None"):
                    stock_val = 0
                else:
                    stock_val = int(float(str(stock).replace(",", ".")))
            except Exception:
                stock_val = 0

            productos.append({
                "iid": iid,
                "codigo": str(vals[0]).strip() if len(vals) > 0 else "",
                "nombre": str(vals[1]).strip() if len(vals) > 1 else "",
                "categoria": str(vals[2]).strip() if len(vals) > 2 else "",
                "descripcion": str(vals[3]).strip() if len(vals) > 3 else "",
                "precio": precio_val,
                "stock": stock_val
            })

        if not productos:
            messagebox.showinfo("Importar", "No hay productos válidos para importar.")
            return

        # 3) realizar import: obtener user_id y abrir conexión para gestionar categorías
        user_id = self._obtener_user_id()
        inserted = []
        errores = []

        try:
            conn = sqlite3.connect(DB_PATH, timeout=10)
            # mantenemos la conexión para _categoria_to_id (esa función usa la conexión pasada)
            for p in productos:
                codigo = p["codigo"]
                nombre = p["nombre"] or "Sin nombre"
                descripcion = p["descripcion"] or ""
                precio_val = p["precio"]
                stock_val = p["stock"]

                # obtener categoria_id (si no existe, asigna a 'Otros' con id 10 o lo crea)
                try:
                    categoria_id = self._categoria_to_id(p["categoria"], conn)
                except Exception as e:
                    errores.append((codigo, f"Error al resolver categoría: {e}"))
                    continue

                # Insert producto usando tu controlador (add_product hace su propio commit)
                try:
                    id_producto = controlador_producto.add_product(codigo, nombre, descripcion, precio_val, categoria_id)
                except ValueError as ve:
                    # por ejemplo: código duplicado ya en DB
                    errores.append((codigo, str(ve)))
                    continue
                except Exception as e:
                    errores.append((codigo, f"Error insert producto: {e}"))
                    continue

                # Registrar movimiento inicial para fijar stock
                try:
                    controlador_movimiento.registrar_movimiento(id_producto, user_id, "inicial", stock_val)
                except Exception as e:
                    # si falla el registro de movimiento, lo reportamos (producto quedó insertado)
                    errores.append((codigo, f"Producto insertado (id {id_producto}) pero fallo registro stock: {e}"))
                    # decidir: continuar con siguientes productos
                    continue

                # si llegamos aquí todo OK para este producto
                inserted.append((p["iid"], codigo))

        finally:
            try:
                conn.close()
            except:
                pass

        # 4) eliminar de la vista los insertados con éxito
        for iid, codigo in inserted:
            try:
                # antes de eliminar comprobamos que el iid exista (puede haberse modificado)
                if iid in self.tree.get_children():
                    self.tree.delete(iid)
            except Exception:
                # si falla, ignoramos (no crítico)
                pass

        # 5) mostrar resumen
        resumen = f"Importación finalizada.\nProductos insertados: {len(inserted)}."
        if errores:
            resumen += f"\nErrores: {len(errores)}. Ejemplos: {errores[:6]}"
        messagebox.showinfo("Resumen importación", resumen)

        # actualizar estado del botón importar y demás
        self.actualizar_estado_importar()

        if inserted:
            self.destroy()

    def mostrar_ejemplo(self):
        """Muestra un ejemplo corto de CSV y permite guardarlo."""
        ejemplo_lines = [
            ["codigo","nombre","nombre_categoria","descripcion","precio","stock"],
            ["E001","Ejemplo Arroz 1kg","Abarrotes","Arroz ejemplo 1kg","3200.00","50"],
            ["E002","Ejemplo Jugo 1L","Bebidas","Jugo natural ejemplo","5200,50","30"],
            ["E003","Ejemplo Pan 400g","Panadería","Pan ejemplo","4800","20"],
        ]

        top = tk.Toplevel(self)
        top.title("Ejemplo CSV")
        top.geometry("600x260")
        tk.Label(top, text="Ejemplo de archivo CSV válido (puedes guardarlo):", font=("Arial", 11)).pack(pady=6)

        # Mostrar como texto con líneas separadas
        txt = tk.Text(top, height=8, wrap="none")
        # construir texto en formato CSV con coma como separador (más legible)
        csv_text = "\n".join([",".join(row) for row in ejemplo_lines])
        txt.insert("1.0", csv_text)
        txt.configure(state="disabled")
        txt.pack(fill="both", expand=True, padx=8, pady=6)

        btn_frame = tk.Frame(top)
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Guardar ejemplo como CSV", command=lambda: self.guardar_ejemplo(ejemplo_lines)).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cerrar", command=top.destroy).pack(side="left", padx=6)

    def guardar_ejemplo(self, rows):
        """Guarda el ejemplo (lista de filas) en un CSV que el usuario elija."""
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile="ejemplo_productos.csv")
        if not path:
            return
        try:
            import csv
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for row in rows:
                    writer.writerow(row)
            messagebox.showinfo("Guardado", f"Ejemplo guardado en:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el ejemplo:\n{e}")

class VentanaExportar(tk.Toplevel):
    """
    Ventana para exportar productos de la base de datos a CSV o Excel.
    """

    def __init__(self, master, main_app=None):
        super().__init__(master)
        self.main_app = main_app
        self.title("Exportar Productos")
        self.geometry("400x250")
        self.centrar_ventana(400, 300)
        self.iconphoto(False, tk.PhotoImage(file="assets/images/Logo_icon.png"))

        # Canvas principal
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#B6B6B6")
        self.canvas.pack(fill="both", expand=True)

        # Fondo con logo
        try:
            self.logo_tk = ImageTk.PhotoImage(
                Image.open("assets/images/Logo_BG.png").convert("RGBA")
            )
            self.logo_item = self.canvas.create_image(0, 0, image=self.logo_tk, anchor="center")
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            self.logo_item = None

        # Título
        self.text_titulo = self.canvas.create_text(
            0, 0,
            text="Exportar productos",
            fill="black",
            font=("Arial", 16, "bold")
        )

        # Botones
        self.btn_csv = tk.Button(
            self, text="Exportar como CSV",
            command=self.exportar_csv,
            font=("Arial", 12)
        )
        self.btn_csv_item = self.canvas.create_window(0, 0, window=self.btn_csv)

        self.btn_excel = tk.Button(
            self, text="Exportar como Excel",
            command=self.exportar_excel,
            font=("Arial", 12)
        )
        self.btn_excel_item = self.canvas.create_window(0, 0, window=self.btn_excel)

        # Reubicar al cambiar tamaño
        self.bind("<Configure>", self.reubicar_elementos)

    def reubicar_elementos(self, event=None):
        """Centrar el contenido en la ventana"""
        w = self.winfo_width()
        h = self.winfo_height()
        cx, cy = w // 2, h // 2

        if self.logo_item:
            self.canvas.coords(self.logo_item, cx, cy)

        self.canvas.coords(self.text_titulo, cx, cy - 60)
        self.canvas.coords(self.btn_csv_item, cx, cy)
        self.canvas.coords(self.btn_excel_item, cx, cy + 50)

    def centrar_ventana(self, ancho=300, alto=400):
        """Centrar ventana en la pantalla"""
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    # --- Exportar como CSV ---
    def exportar_csv(self):
        productos = controlador_producto.get_all_products()
        if not productos:
            messagebox.showinfo("Exportar", "No hay productos para exportar.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Guardar archivo como",
            initialfile="productos_exportados.csv"
        )
        if not file_path:
            self.destroy()
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["codigo", "nombre", "nombre_categoria", "descripcion", "precio", "stock"])
                for p in productos:
                    writer.writerow([
                        p.get("codigo", ""),
                        p.get("nombre", ""),
                        p.get("nombre_categoria", ""),
                        p.get("descripcion", ""),
                        p.get("precio", ""),
                        p.get("stock", "")
                    ])
            messagebox.showinfo("Exportar", f"Productos exportados en:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el CSV:\n{e}")
        
        self.destroy()

    # --- Exportar como Excel ---
    def exportar_excel(self):
        productos = controlador_producto.get_all_products()
        if not productos:
            messagebox.showinfo("Exportar", "No hay productos para exportar.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Guardar archivo como",
            initialfile="productos_exportados.xlsx"
        )
        if not file_path:
            self.destroy()
            return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Productos"

            ws.append(["codigo", "nombre", "nombre_categoria", "descripcion", "precio", "stock"])
            for p in productos:
                ws.append([
                    p.get("codigo", ""),
                    p.get("nombre", ""),
                    p.get("nombre_categoria", ""),
                    p.get("descripcion", ""),
                    p.get("precio", ""),
                    p.get("stock", "")
                ])

            wb.save(file_path)
            messagebox.showinfo("Exportar", f"Productos exportados en:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el Excel:\n{e}")
        
        self.destroy()