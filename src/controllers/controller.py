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

def ingresar_usuario(usuario, password, rol):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Usuarios (usuario, password, rol) VALUES (?, ?, ?)",
                   (usuario, password, rol))
    conn.commit()
    conn.close()

def movimiento_ingreso (id_produc,id_usuar,tip,cant):
    if tip == "entrada" or tip == "salida":
        print("Es un movimiento valido")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Movimientos (id_producto,id_usuario,tipo,cantidad) VALUES (?,?,?,?)",
                       (id_produc,id_usuar,tip,cant))
        conn.commit()
        conn.close()
        return 'exitoso'
    else:
        print("Invalido")

#genera una lista de todos los productos
def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos")
    productos = cursor.fetchall()
    conn.close()
    print(productos)
    return productos




insertar_producto("Banano", "Fruta", 1000, 100, 1001)
#ingresar_usuario("juan","password123","empleado")
movimiento_ingreso(1,1,'entrada',10)
obtener_productos()