import tkinter
from tkinter import messagebox
from src.controllers import controlador_usuario
from src.views.main_view import MainApp   # <-- importa la ventana principal

# ejecutar vista python -m src.views.login_view

class LoginApp:

    # log es la ventana de login
    def __init__(self, log):

        ancho=400
        alto=400
        #centrar ventana en la pantalla
        ancho_pantalla = log.winfo_screenwidth()
        alto_pantalla = log.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)

        self.log = log
        self.log.title("Login - Gestor de Inventario")
        self.log.geometry(f"{ancho}x{alto}+{x}+{y}")
        print("Pagina de Login Iniciada.")
        color="#B6B6B6"
        colorLetra="#000000"
         #Color de fondo de la ventana
        self.log.config(bg=color)
        #Creando el Frame de login dentro de la ventana Log 
        frame = tkinter.Frame(bg=color)
        frame.winfo_geometry()

        #Creando los wdigets
        self.login_label = tkinter.Label(frame, text="Iniciar Sesión",bg=color, fg="#210ed1", font=("Arial", 30))
        #Usuario
        self.nombre_label = tkinter.Label(frame, text="Usuario:", bg=color, fg=colorLetra, font=("Arial", 16))
        self.acceso_usuario = tkinter.Entry(frame, font=("Arial", 16))
        #Contraseña
        self.contraseña_label = tkinter.Label(frame, text="Contraseña:", bg=color, fg=colorLetra, font=("Arial", 16))
        self.password_acceso = tkinter.Entry(frame, show="*", font=("Arial", 16))
        #Boton de login
        self.login_button = tkinter.Button(frame, text="Ingresar", command=self.validar, bg="#210ed1", fg="white", font=("Arial", 16))


        #Colocando los widgets en la ventana
        self.login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        #usuario
        self.nombre_label.grid(row=1, column=0)
        self.acceso_usuario.grid(row=1, column=1, pady=10) 
        #contraseña
        self.contraseña_label.grid(row=2, column=0)
        self.password_acceso.grid(row=2, column=1, pady=10)
        #boton
        self.login_button.grid(row=3, column=0, columnspan=2, pady=30)

        frame.pack()


     


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