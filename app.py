import tkinter as tk
from src.views.login_view import LoginApp

if __name__ == "__main__":
    ventana_login = tk.Tk()
    app = LoginApp(ventana_login)
    ventana_login.mainloop()