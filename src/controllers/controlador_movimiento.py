import sqlite3 as sql
import os
from datetime import datetime
from src.utils.path_utils import resource_path

db_path = resource_path("data/inventario.db")

def get_connection():
    # Agregamos timeout para esperar si la DB está ocupada
    return sql.connect(db_path, timeout=10)

def registrar_movimiento(id_producto, id_usuario, tipo, cantidad):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Insertar movimiento
        cursor.execute("""
            INSERT INTO Movimientos (id_producto, id_usuario, tipo, cantidad, fecha_registro)
            VALUES (?, ?, ?, ?, ?)
        """, (id_producto, id_usuario, tipo, cantidad, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # obtener stock actual
        cursor.execute("SELECT cantidad FROM Stock WHERE id_producto = ?", (id_producto,))
        result = cursor.fetchone()

        if result is None:
            raise ValueError(f"No existe stock registrado para el producto con id {id_producto}")

        stock_actual = result[0]

        # calcular nuevo stock
        if tipo == "entrada":
            nuevo_stock = stock_actual + cantidad
        elif tipo == "salida":
            if cantidad > stock_actual:
                raise ValueError("No hay suficiente stock para realizar la salida.")
            nuevo_stock = stock_actual - cantidad
        elif tipo == "inicial":
            nuevo_stock = cantidad
        elif tipo == "ajuste":
            nuevo_stock = cantidad
        else:
            raise ValueError(f"Tipo de movimiento no válido: {tipo}")

        # verifico que no quede stock negativo
        if nuevo_stock < 0:
            raise ValueError("Stock insuficiente para salida")

        # actualizar stock si todo esta correcto
        cursor.execute("UPDATE Stock SET cantidad = ? WHERE id_producto = ?", (nuevo_stock, id_producto))

        conn.commit()