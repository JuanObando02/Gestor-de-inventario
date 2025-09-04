import tkinter
from tkinter import messagebox
from src.controllers import controlador_usuario
from src.views.main_view import MainApp   # <-- importa la ventana principal

# ejecutar vista python -m src.views.login_view

class LoginApp:

    # log es la ventana de login
    def __init__(self, log):
        self.log = log
        self.log.title("Login - Gestor de Inventario")
        self.log.geometry("300x180")
        print("Pagina de Login Iniciada.")

        # Usuario
        tkinter.Label(log, text="Usuario:").pack(pady=5)
        self.acceso_usuario = tkinter.Entry(log)
        self.acceso_usuario.pack()

        # Contraseña
        tkinter.Label(log, text="Contraseña:").pack(pady=5)
        self.password_acceso = tkinter.Entry(log, show="*")
        self.password_acceso.pack()

        # Botón
        tkinter.Button(log, text="Ingresar", command=self.validar).pack(pady=10)

    def validar(self):
        #solicitamos datos de ingreso.
        usuario = self.acceso_usuario.get()
        password = self.password_acceso.get()

        #Validamos con nuestro controlador el usuario ingresado y la contraseña con la base de datos
        user = controlador_usuario.validate_login(usuario, password)

        #Si se retorno un usuario:
        if user:
            messagebox.showinfo("Éxito", f"Bienvenido {user.username} ({user.role})")
            self.log.destroy()  # cerrar login
            print("Claves de acceso correctas, Login Cerrado.")

            # Crear la nueva ventana principal
            new_root = tkinter.Tk()
            MainApp(new_root, user)
            new_root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            print("Claves de acceso Incorrectar. Intente nuevamente.")


if __name__ == "__main__":
    ventana = tkinter.Tk()
    app = LoginApp(ventana)
    ventana.mainloop()