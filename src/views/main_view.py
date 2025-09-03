import tkinter as tk

class MainApp:
    def __init__(self, root, user):
        self.root = root
        self.root.title("Gestor de Inventario")
        self.root.geometry("600x400")

        # Bienvenida
        label = tk.Label(root, text=f"Bienvenido {user.username} ({user.role})", font=("Arial", 14))
        label.pack(pady=20)

        # Botón de salir
        tk.Button(root, text="Cerrar sesión", command=self.root.quit).pack(pady=10)

        # Aquí podrías agregar botones para ir a: Productos, Categorías, Ventas, etc.
        tk.Button(root, text="Gestión de Productos", command=self.gestion_productos).pack(pady=5)
        tk.Button(root, text="Gestión de Usuarios", command=self.gestion_usuarios).pack(pady=5)

    def gestion_productos(self):
        # Aquí luego abrirás otra ventana o frame
        print("Abrir gestión de productos")

    def gestion_usuarios(self):
        # Aquí luego abrirás otra ventana o frame
        print("Abrir gestión de usuarios")