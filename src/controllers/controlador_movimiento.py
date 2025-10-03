import sqlite3 as sql
import os
from datetime import datetime
from src.utils.path_utils import resource_path

db_path = resource_path("data/inventario.db")

def get_connection():
    return sql.connect(db_path, timeout=10)

def registrar_movimiento(id_producto, id_usuario, tipo, cantidad):
    # El 'with' garantiza que la conexión se cierre (conn.close())
    with get_connection() as conn: 
        # Utilizamos try...except para gestionar la transacción
        try:
            cursor = conn.cursor()

            # 1. Insertar movimiento
            cursor.execute("""
                INSERT INTO Movimientos (id_producto, id_usuario, tipo, cantidad, fecha_registro)
                VALUES (?, ?, ?, ?, ?)
            """, (id_producto, id_usuario, tipo, cantidad, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            # 2. Obtener stock actual y calcular nuevo stock (toda la lógica de cálculo...)
            cursor.execute("SELECT cantidad FROM Stock WHERE id_producto = ?", (id_producto,))
            result = cursor.fetchone()

            if result is None:
                raise ValueError(f"No existe stock registrado para el producto con id {id_producto}")
            
            stock_actual = result[0]
            # ... Lógica de cálculo del nuevo_stock ...
            if tipo == "entrada":
                nuevo_stock = stock_actual + cantidad
            elif tipo == "salida":
                if cantidad > stock_actual:
                    raise ValueError("No hay suficiente stock para realizar la salida.")
                nuevo_stock = stock_actual - cantidad
            # ... otros tipos ...
            else:
                raise ValueError(f"Tipo de movimiento no válido: {tipo}")
            
            # Verificar stock negativo
            if nuevo_stock < 0:
                 raise ValueError("Stock insuficiente para salida")

            # 3. Actualizar stock si todo esta correcto
            cursor.execute("UPDATE Stock SET cantidad = ? WHERE id_producto = ?", (nuevo_stock, id_producto))
            
            # 4. Si llegamos aquí sin errores, CONFIRMAR los cambios
            conn.commit() 
            
            print(f"Movimiento de {tipo} registrado para producto {id_producto}. Nuevo stock: {nuevo_stock}")

        except Exception as e:
            # 5. Si ocurre CUALQUIER error, DESHACER los cambios pendientes
            conn.rollback() 
            print(f"ERROR: {e}. Transacción revertida (Rollback).")
            # Re-lanza la excepción para que el programa que llamó a la función sepa que falló
            raise e 
            
# Al salir del 'with', conn.close() se ejecuta automáticamente.