import sqlite3 as sql
import hashlib, os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.models.user import User

db_path = os.path.join("data", "inventario.db")

def get_connection(): 
    return sql.connect(db_path, timeout=10)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
#se usa sha256 para hashear la contraseña y encode para convertirla a bytes.
#con hexdigest se obtiene la representacion en hexadecimal del hash.
# se usa sha256 para hashear la contraseña y encode para convertirla a bytes.
# con hexdigest se obtiene la representacion en hexadecimal del hash.

def insert_user(username, password, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Usuarios (usuario, password, rol) VALUES (?, ?, ?)",
        (username, hash_password(password), role)
    )
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_usuario, usuario, password, rol FROM usuarios WHERE usuario = ?",
        (username,)
    )

    row = cur.fetchone()
    conn.close()
    
    #si row no es None, crea y retorna un objeto User
    if row:
        return User(*row)
    return None

def validate_login(username, password):
    user = get_user(username)
    # validar si el usuario fue retornado y si la contraseña hasheada coincide. 
    if user and user.password == hash_password(password):
        return user
    return None
