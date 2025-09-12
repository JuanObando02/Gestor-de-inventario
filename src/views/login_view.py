import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
from src.controllers import controlador_usuario
from src.views.main_view import MainApp   # <-- importa la ventana principal

# ejecutar vista python -m src.views.login_view

class LoginApp:

    # log es la ventana de login
    def __init__(self, log):
        self.log = log
        self.log.title("Login - Gestor de Inventario")
        self.log.geometry("300x300")
        self.log.configure(bg="#B6B6B6")
        self.log.iconphoto(False, tkinter.PhotoImage(file="src/views/components/Logo (2).png"))
        print("Login")

        ruta_logo = "src/views/components/Logo.png"
        imagen = Image.open(ruta_logo)
        imagen = imagen.resize((100, 100))  # redimensionar
        self.logo_img = ImageTk.PhotoImage(imagen)
        tkinter.Label(log, image=self.logo_img, bg="#B6B6B6").pack(pady=10)
        
        # Usuario
        tkinter.Label(log, text="Usuario:",bg="#B6B6B6").pack(pady=5)
        self.acceso_usuario = tkinter.Entry(log)
        self.acceso_usuario.pack()

        # Contraseña
        tkinter.Label(log, text="Contraseña:", bg="#B6B6B6").pack(pady=5)
        self.password_acceso = tkinter.Entry(log, show="*")
        self.password_acceso.pack()

        # Botón
        tkinter.Button(log, text="Ingresar", command=self.validar, bg="#210ed1", fg="white").pack(pady=10)

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