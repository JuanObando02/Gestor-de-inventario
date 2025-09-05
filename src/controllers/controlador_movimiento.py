import sqlite3 as sql
import os
from datetime import datetime

db_path = os.path.join("data", "inventario.db")

def get_connection():
    return sql.connect(db_path)

def registrar_movimiento(id_producto, id_usuario, tipo, cantidad):
    
    conn = get_connection()
    cursor = conn.cursor()

    # Insertar movimiento
    cursor.execute("""
        INSERT INTO Movimientos (id_producto, id_usuario, tipo, cantidad, fecha_registro)
        VALUES (?, ?, ?, ?, ?)
    """, (id_producto, id_usuario, tipo, cantidad, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # obtener stock actual
    cursor.execute("SELECT cantidad FROM Stock WHERE id_producto = ?", (id_producto,))
    result = cursor.fetchone()
    # tupla (cantidad,)

    stock_actual = result[0]
    # si es entrada sumo, si es salida resto
    nuevo_stock = stock_actual + cantidad if tipo == "entrada" else stock_actual - cantidad
    
    # verifico que no quede stock negativo
    if nuevo_stock < 0:
        # Si el stock resultante es negativo, revertir los cambios y lanzar error
        conn.rollback()
        conn.close()
        raise ValueError("Stock insuficiente para salida")
    
    # actualizar stock si todo esta correcto
    cursor.execute("UPDATE Stock SET cantidad = ? WHERE id_producto = ?", (nuevo_stock, id_producto))

    conn.commit()
    conn.close()
