from src.views.login_view import login_interface
import tkinter as tk

def main():
    user = None
    while not user:  # repite hasta que loguee bien
        user = login_interface()

    # Aquí podrías ir a otro menú según el rol
    print("Accediendo al sistema...")

if __name__ == "__main__":
    main()