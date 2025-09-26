import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import controlador_producto, controlador_movimiento
from PIL import Image, ImageTk

class VentanaMovimientos(tk.Toplevel):
    def __init__(self, parent, user, on_complete_callback):
        super().__init__(parent)
        self.title("Registrar Movimiento de Inventario")
        self.geometry("400x350")
        self.user = user
        self.on_complete_callback = on_complete_callback # Guarda la referencia a la función
        self.centrar_ventana(400, 350)
        self.iconphoto(False, tk.PhotoImage(file="assets/images/Logo_icon.png"))
        self.config(bg="#B6B6B6")
         # Fondo con imagen/logo
        # =====================
        try:
            logo = Image.open("assets/images/Logo_con_nombre_100x126.png").convert("RGBA")  # logo con transparencia
            logo = logo.resize((200, 200), Image.LANCZOS)  # Ajustar tamaño
            # Crear un nuevo canal alfa con menos opacidad
            
            self.logo_tk = ImageTk.PhotoImage(logo)
            
            # Colocar en la ventana
            self.bg_label = tk.Label(self, image=self.logo_tk, bg="#B6B6B6")
            self.bg_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")

        # Frame para los widgets encima del fondo
        frame = tk.Frame(self, bg="#B6B6B6")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Producto
        tk.Label(self, text="Producto:").pack(pady=5)
        self.productos = controlador_producto.get_all_products()  # Consulto todos los productos de la DB
        self.producto_cb = ttk.Combobox(
            self,
            values=[f"{p['codigo']} - {p['nombre']}" for p in self.productos],
            state="readonly",
            width=30
        )
        self.producto_cb.pack()



        # Tipo de movimiento
        tk.Label(self, text="Tipo de movimiento:").pack(pady=5)
        self.tipo_cb = ttk.Combobox(
            self,
            values=["entrada", "salida"],
            state="readonly",
            width=20
        )
        self.tipo_cb.pack()

        # Cantidad
        tk.Label(self, text="Cantidad:").pack(pady=5)
        self.cantidad_entry = tk.Entry(self)
        self.cantidad_entry.pack()

        # Botón registrar
        tk.Button(self, text="Registrar", command=self.registrar).pack(pady=20)
    
    def centrar_ventana(self, ancho=300, alto=400):
        """Centrar ventana en la pantalla"""
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def registrar(self):
        try:
            producto_index = self.producto_cb.current()
            if producto_index == -1:
                messagebox.showerror("Error", "Debe seleccionar un producto")
                return

            producto = self.productos[producto_index]
            tipo = self.tipo_cb.get()
            if not tipo:
                messagebox.showerror("Error", "Debe seleccionar tipo de movimiento")
                return

            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return

            # Guardar movimiento en la DB
            controlador_movimiento.registrar_movimiento(
                id_producto = producto['id_producto'],
                id_usuario=self.user.id_user,
                tipo=tipo,
                cantidad=cantidad
            )

            messagebox.showinfo("Éxito", f"{tipo.capitalize()} registrada para {producto['nombre']}")

            # Llama al callback para actualizar la tabla principal
            if self.on_complete_callback:
                self.on_complete_callback()
            self.destroy()
                   

        except ValueError as e:
             messagebox.showerror("Error", str(e))
            

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
