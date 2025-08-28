import tkinter as tk
from tkinter import messagebox
import json
from app import App  # Importamos la clase App de la ventana principal

class Login:
    def __init__(self, root): #constructor
        self.root = root
        self.root.title("Login - Gestor de Inventario")
        self.root.geometry("300x150")

        # Cargar usuarios desde JSON
        with open("usuarios.json", "r") as f:
            self.usuarios = json.load(f)

        # UI
        tk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(root)
        self.entry_user.pack()

        tk.Label(root, text="Contraseña:").pack(pady=5)
        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.pack()

        tk.Button(root, text="Ingresar", command=self.validar_login).pack(pady=10)

    def validar_login(self):
        usuario = self.entry_user.get()
        clave = self.entry_pass.get()

        for u in self.usuarios:
            if u["usuario"] == usuario and u["password"] == clave:
                rol = u["rol"]
                self.root.destroy()
                self.abrir_app(rol)
                return

        messagebox.showerror("Error", "Credenciales incorrectas")

    def abrir_app(self, rol):
        main_root = tk.Tk()
        App(main_root, rol)  # Pasamos el rol al App
        main_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    login = Login(root)
    root.mainloop()
