import sqlite3 as sql
import hashlib, os, sys
from src.models.user import User
from src.utils.path_utils import resource_path

db_path = resource_path("data/inventario.db")

def get_connection(): 
    return sql.connect(db_path, timeout=10)

def hash_password(password):
    """Hash SHA-256 de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def insert_user(username, password, role):
    """Inserta un usuario. Lanza la excepción de sqlite si falla (p. ej. UNIQUE)."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Usuarios (usuario, password, rol) VALUES (?, ?, ?)",
            (username, hash_password(password), role)
        )

def get_user(username):
    """Devuelve un objeto User o None"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id_usuario, usuario, password, rol FROM Usuarios WHERE usuario = ?",
            (username,)
        )
        row = cur.fetchone()
    if row:
        return User(*row)
    return None

def validate_login(username, password):
    """Valida credenciales y devuelve el User si son correctas"""
    user = get_user(username)
    if user.password == hash_password(password):
        return user
    return None

def list_users():
    """Devuelve una lista de todos los usuarios como tuplas (id_usuario, usuario, rol)"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, usuario, rol FROM Usuarios")
        rows = cur.fetchall()
    return rows

def update_user(usuario, password, rol):
    """Actualiza la contraseña y/o rol de un usuario"""
    with get_connection() as conn:
        cur = conn.cursor()
        if password:  # actualizar también contraseña si se proporciona
            cur.execute(
                "UPDATE Usuarios SET password = ?, rol = ? WHERE usuario = ?",
                (hash_password(password), rol, usuario)
            )
        else:
            cur.execute("UPDATE Usuarios SET rol = ? WHERE usuario = ?", (rol, usuario))
        # commit implícito

def delete_user(id_usuario):
    """Elimina un usuario por id"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM Usuarios WHERE id_usuario = ?", (id_usuario,))