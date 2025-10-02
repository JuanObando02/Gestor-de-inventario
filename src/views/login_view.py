import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
from src.controllers import controlador_usuario
from src.views.main_view import MainApp   # <-- importa la ventana principal
from src.utils.path_utils import resource_path
# ejecutar vista python -m src.views.login_view

class LoginApp:

    # log es la ventana de login
    def __init__(self, log):

        ancho = 400
        alto = 400
        # centrar ventana en la pantalla
        ancho_pantalla = log.winfo_screenwidth()
        alto_pantalla = log.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)

        self.log = log
        self.log.title("Login - Gestor de Inventario")
        self.centrar_ventana(300, 300)
        self.log.configure(bg="#B6B6B6")

        # --- ICONO ventana: guardar la referencia en self para evitar GC ---
        try:
            icon_path = resource_path("assets/images/Logo_icon.png")
            self._icon_img = tkinter.PhotoImage(file=icon_path)  # guardar
            log.iconphoto(False, self._icon_img)
        except Exception as e:
            print("No se pudo cargar icono:", e)

        # --- cargar logo con PIL y convertir a ImageTk, guardar referencia ---
        try:
            logo_path = resource_path("assets/images/Logo_con_nombre_100x126.png")
            pil_logo = Image.open(logo_path)
            self.logo_img = ImageTk.PhotoImage(pil_logo)   # MUY IMPORTANTE: ImageTk.PhotoImage
            lbl_logo = tkinter.Label(log, image=self.logo_img, bg="#B6B6B6")
            lbl_logo.pack(pady=10)
            lbl_logo.image = self.logo_img  # refer. adicional (seguridad)
        except Exception as e:
            print("No se pudo cargar el logo:", e)
            # como fallback, mostrar texto
            tkinter.Label(log, text="Gestor de Inventario", bg="#B6B6B6", font=("Arial", 14)).pack(pady=20)

        # Usuario
        tkinter.Label(log, text="Usuario:", bg="#B6B6B6").pack(pady=5)
        self.acceso_usuario = tkinter.Entry(log)
        self.acceso_usuario.pack()

        # Contraseña
        tkinter.Label(log, text="Contraseña:", bg="#B6B6B6").pack(pady=5)

        # Crear un Frame para contener el Entry y el Button uno al lado del otro
        frame_password = tkinter.Frame(log, bg="#B6B6B6")
        frame_password.pack()

        self.password_acceso = tkinter.Entry(frame_password, show="*", width=15)
        self.password_acceso.pack(side="left")

        self.mostrar_password = False
        self.btn_mostrar = tkinter.Button(frame_password, text="Ver", command=self.mostrar, bg="#9C9B9B", relief="raised")
        self.btn_mostrar.pack(side="left", padx=2)

        # Botón
        tkinter.Button(log, text="Ingresar", command=self.validar, bg="#357BB7", fg="white").pack(pady=10)

        # Permitir login con Enter
        self.log.bind("<Return>", lambda event: self.validar())

    # ejemplo de centrar_ventana (si no la tienes definida)
    def centrar_ventana(self, ancho, alto):
        ancho_pantalla = self.log.winfo_screenwidth()
        alto_pantalla = self.log.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.log.geometry(f"{ancho}x{alto}+{x}+{y}")

    # placeholder mostrar y validar (mantener tus implementaciones)
    def mostrar(self):
        """Mostrar/ocultar contraseña"""
        if self.mostrar_password:
            self.password_acceso.config(show="*")
            self.btn_mostrar.config(text="Ver")
            self.mostrar_password = False
        else:
            self.password_acceso.config(show="")
            self.btn_mostrar.config(text="Ocultar")
            self.mostrar_password = True

    def validar(self):
        #solicitamos datos de ingreso.
        usuario = self.acceso_usuario.get()
        password = self.password_acceso.get()

        #Validamos con nuestro controlador el usuario ingresado y la contraseña con la base de datos
        user = controlador_usuario.validate_login(usuario, password)

        #Si se retorno un usuario:
        if user:
            messagebox.showinfo("Éxito", f"Bienvenido al Gestor de Inventarios Mini Stock ,{user.username}")
            self.log.destroy()  # cerrar login
            print("Claves de acceso correctas, Login Cerrado.")

            # Crear la nueva ventana principal
            ventana_menu = tkinter.Tk()
            MainApp(ventana_menu, user)
            ventana_menu.mainloop()
            
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            print("Claves de acceso Incorrectar. Intente nuevamente.")
