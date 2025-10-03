import sqlite3 as sql
import os
from src.models.producto import Producto
from src.utils.path_utils import resource_path

db_path = resource_path("data/inventario.db")

def get_connection():
    return sql.connect(db_path, timeout=5)

#agregar un producto a la base de datos
def add_product(codigo, nombre, descripcion, precio, categoria_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO Productos (codigo, nombre, descripcion, precio, id_categoria)
                   VALUES (?, ?, ?, ?, ?)""",
                (codigo, nombre, descripcion, precio, categoria_id)
            )
            id_producto = cur.lastrowid
            cur.execute(
                "INSERT INTO Stock (id_producto, cantidad) VALUES (?, 0)",
                (id_producto,)
            )
            return id_producto
        
    except sql.IntegrityError as e:

        if "UNIQUE constraint failed" in str(e):
            raise ValueError(f"El código '{codigo}' ya existe. Debe ser único.")
        else:
            raise

# eliminar un producto de la base de datos
def delete_product(id_producto):
    with get_connection() as conn:
        cur = conn.cursor()

        # Verificar stock
        cur.execute("SELECT cantidad FROM Stock WHERE id_producto = ?", (id_producto,))
        result = cur.fetchone()
        if result and result[0] > 0:
            raise ValueError("No se puede eliminar un producto con stock disponible.")

        # Eliminar primero el registro en Stock
        cur.execute("DELETE FROM Stock WHERE id_producto = ?", (id_producto,))
        # También eliminar movimientos
        cur.execute("DELETE FROM Movimientos WHERE id_producto = ?", (id_producto,))
        # Finalmente eliminar producto
        cur.execute("DELETE FROM Productos WHERE id_producto = ?", (id_producto,))

        conn.commit()

# actualizar un producto en la base de datos
def update_product(id_producto, codigo, nombre, descripcion, precio, categoria_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """UPDATE Productos
                   SET codigo = ?,
                       nombre = ?,
                       descripcion = ?,
                       precio = ?,
                       id_categoria = ?
                   WHERE id_producto = ?""",
                (codigo, nombre, descripcion, precio, categoria_id, id_producto)
            )
            conn.commit()

            if cur.rowcount == 0:
                raise ValueError(f"No se encontró el producto con ID {id_producto}")

    except sql.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise ValueError(f"El código '{codigo}' ya existe. Debe ser único.")
        else:
            raise

# obtener todos los productos
def get_all_products():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
                SELECT p.id_producto, p.codigo, p.nombre, p.id_categoria, p.descripcion, p.precio,
                    s.cantidad, c.nombre AS nombre_categoria
                FROM Productos p
                LEFT JOIN Stock s ON p.id_producto = s.id_producto
                LEFT JOIN Categorias c ON p.id_categoria = c.id_categoria
            """)

        rows = cur.fetchall()

    # convertimos las tuplas en diccionarios
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
    return productos