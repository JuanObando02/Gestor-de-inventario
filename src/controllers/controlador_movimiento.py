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
    
    # calcular nuevo stock
    if tipo == "entrada":
        nuevo_stock = stock_actual + cantidad
    elif tipo == "salida":
        if cantidad > stock_actual:
            raise ValueError("No hay suficiente stock para realizar la salida.")
        nuevo_stock = stock_actual - cantidad
    elif tipo == "inicial":
        # Para el registro inicial del producto
        nuevo_stock = cantidad
    elif tipo == "ajuste":
        # Para correcciones manuales de inventario
        nuevo_stock = cantidad
    else:
        raise ValueError(f"Tipo de movimiento no válido: {tipo}")
    
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
