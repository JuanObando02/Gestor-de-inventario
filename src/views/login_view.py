import tkinter as tk
from tkinter import messagebox
from src.controllers import controlador_usuario
from src.views.main_view import MainApp

class LoginApp:
<<<<<<< Updated upstream
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
=======

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
        color="#333333"
        self.log.config(bg=color)
        #Creando el Frame de login dentro de la ventana Log 
        frame = tkinter.Frame(bg=color)
        frame.winfo_geometry()

        #Creando los wdigets
        self.login_label = tkinter.Label(frame, text="Iniciar Sesión",bg=color, fg="#1D80AB", font=("Arial", 30))
        #Usuario
        self.nombre_label = tkinter.Label(frame, text="Usuario:", bg=color, fg="white", font=("Arial", 16))
        self.acceso_usuario = tkinter.Entry(frame, font=("Arial", 16))
        #Contraseña
        self.contraseña_label = tkinter.Label(frame, text="Contraseña:", bg=color, fg="white", font=("Arial", 16))
        self.password_acceso = tkinter.Entry(frame, show="*", font=("Arial", 16))
        #Boton de login
        self.login_button = tkinter.Button(frame, text="Ingresar", command=self.validar, bg="#148CBF", fg="white", font=("Arial", 16))


        #Colocando los widgets en la ventana
        self.login_label.grid(row=0, column=1, columnspan=2, sticky="news", pady=40)
        #usuario
        self.nombre_label.grid(row=1, column=0)
        self.acceso_usuario.grid(row=1, column=1, pady=10) 
        #contraseña
        self.contraseña_label.grid(row=2, column=0)
        self.password_acceso.grid(row=2, column=1, pady=10)
        #boton
        self.login_button.grid(row=3, column=0, columnspan=2, pady=30)
<<<<<<< Updated upstream
=======

        frame.pack()


     

>>>>>>> Stashed changes

        frame.pack()


     

>>>>>>> Stashed changes

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