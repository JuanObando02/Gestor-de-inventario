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
    try:
        # Insertar producto
        cur.execute(
            """INSERT INTO Productos (codigo, nombre, descripcion, precio, id_categoria)
               VALUES (?, ?, ?, ?, ?)""",
            (codigo, nombre, descripcion, precio, categoria_id)
        )

        id_producto = cur.lastrowid

        # Inicializar stock en 0
        cur.execute(
            "INSERT INTO Stock (id_producto, cantidad) VALUES (?, 0)",
            (id_producto,)
        )

        conn.commit()
        return id_producto
        

    except sql.IntegrityError as e:
        
        # Captura de error si el código ya existe (colisión en UNIQUE)
        if "UNIQUE constraint failed" in str(e):
            raise ValueError(f"El código '{codigo}' ya existe. Debe ser único.")
        else:
            raise
    finally:
        conn.close()

def get_all_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
            SELECT p.id_producto, p.codigo, p.nombre, p.id_categoria, p.descripcion, p.precio,
                s.cantidad, c.nombre AS nombre_categoria
            FROM Productos p
            LEFT JOIN Stock s ON p.id_producto = s.id_producto
            LEFT JOIN Categorias c ON p.id_categoria = c.id_categoria
        """)

    rows = cur.fetchall() #lista de tuplas encontradas
    conn.close()
    
    # convertimos las tuplas en diccionarios para facilitar su uso
    productos = []
    for r in rows:
        productos.append({
            "id_producto": r[0],
            "codigo": r[1],
            "nombre": r[2],
            "categoria_id": r[3],
            "descripcion": r[4],
            "precio": r[5],
            "stock": r[6] if r[6] is not None else 0,
            "nombre_categoria": r[7]
        })
    #retorna la lista de diccionarios
    return productos
