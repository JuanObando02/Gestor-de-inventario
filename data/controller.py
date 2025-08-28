import sqlite3 as sql
import os

# Ruta de la base de datos
db_path = os.path.join("data", "inventario.db")

def get_connection(): #funcion que retorna la conexion a la DB
    conection = sql.connect(db_path) 
    return conection

def insertar_producto(nombre, descripcion, precio, id_categoria, codigo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Productos (nombre, descripcion, precio, id_categoria, codigo) VALUES (?, ?, ?, ?, ?)",
                   (nombre, descripcion, precio, id_categoria, codigo))
    conn.commit()
    conn.close()
