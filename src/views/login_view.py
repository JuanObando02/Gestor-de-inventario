import tkinter as tk
from tkinter import messagebox
from src.controllers import controlador_usuario
from src.views.main_view import MainApp   # <-- importa la ventana principal

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Gestor de Inventario")
        self.root.geometry("300x180")
        print("Pagina de Login Iniciada.")

        # Usuario
        tk.Label(root, text="Usuario:").pack(pady=5)
        self.acceso_usuario = tk.Entry(root)
        self.acceso_usuario.pack()

        # Contraseña
        tk.Label(root, text="Contraseña:").pack(pady=5)
        self.password_acceso = tk.Entry(root, show="*")
        self.password_acceso.pack()

        # Botón
        tk.Button(root, text="Ingresar", command=self.validar_login).pack(pady=10)

    def validar_login(self):
        #solicitamos datos de ingreso.
        usuario = self.acceso_usuario.get()
        password = self.password_acceso.get()

        #Validamos con nuestro controlador el usuario ingresado y la contraseña
        user = controlador_usuario.validate_login(usuario, password)

        #Si se retorno un usuario:
        if user:
            messagebox.showinfo("Éxito", f"Bienvenido {user.username} ({user.role})")
            self.root.destroy()  # cerrar login
            print("Claves de acceso correctas, Login Cerrado.")

            # Crear la nueva ventana principal
            new_root = tk.Tk()
            MainApp(new_root, user)
            new_root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            print("Claves de acceso Incorrectar. Intente nuevamente.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()