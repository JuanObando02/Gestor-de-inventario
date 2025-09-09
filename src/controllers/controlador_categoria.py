import sqlite3 as sql
import os

db_path = os.path.join("data", "inventario.db")

def get_connection():
    return sql.connect(db_path)

# Obtener todas las categorías
def get_all_categorias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_categoria, nombre FROM Categorias")
    categorias = cur.fetchall()  # devuelve lista de tuplas [(1, 'Bebidas'), (2, 'Lácteos'), ...]
    conn.close()
    return categorias