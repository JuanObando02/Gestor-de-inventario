import sqlite3 as sql
import os
from src.models.producto import Producto


db_path = os.path.join("data", "inventario.db")

def get_connection():
    return sql.connect(db_path)

#agregar un producto a la base de datos
def add_product(codigo, nombre, descripcion, precio, categoria_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Productos (codigo, nombre, descripcion, precio, id_categoria)
           VALUES (?, ?, ?, ?, ?)""",
        (codigo, nombre, descripcion, precio, categoria_id)
    )
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Productos")
    rows = cur.fetchall() #lista de tuplas encontradas
    conn.close()
    # convertir cada tupla en un objeto Producto y retornar una lista de productos
    # for row in rows recorre cada tupla en la lista y crea un objeto 
    # Producto con los valores desempaquetados (*row). 

    return [Producto(*row) for row in rows]
