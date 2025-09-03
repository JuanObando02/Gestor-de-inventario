import tkinter as tk
from tkinter import messagebox
from src.controllers import controlador_usuario
from src.views.main_view import MainApp

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Gestor de Inventario")
        self.root.geometry("300x180")

        # Usuario
        tk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(root)
        self.entry_user.pack()

        # Contraseña
        tk.Label(root, text="Contraseña:").pack(pady=5)
        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.pack()

        # Botón
        tk.Button(root, text="Ingresar", command=self.login).pack(pady=10)

    def login(self):
        usuario = self.entry_user.get()
        password = self.entry_pass.get()

        user = controlador_usuario.validate_login(usuario, password)

        if user:
            messagebox.showinfo("Éxito", f"Bienvenido {user.username} rol: ({user.role})")
            self.root.destroy()  # cerrar login
            # Aquí puedes abrir la ventana principal del inventario
            
            # Crear la nueva ventana principal
            new_root = tk.Tk()
            MainApp(new_root, user)
            new_root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()