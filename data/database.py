import sqlite3 as sql
import os

#informacion importante de la DB:
# La tabla el codigo del producto no puede ser el mismo es unico
# La tabla usuarios el usuario es unico.
# tipo de movimiento es entrada o salida. agregar tipo de ajuste.
# la tabla stock la cantidad del producto es not null. 
# se creo admin 1234 pro defecto rol admin para pruebas 
# se crearon categorias aleatoreas para pruebas. 


# Ruta de la base de datos
db_path = os.path.join("data", "inventario.db")

#conn es un objeto que permite la conexion con la DB
conn = sql.connect(db_path)
cursor = conn.cursor()

#Se crea la tabla categorias
cursor.execute (
    """ CREATE TABLE IF NOT EXISTS Categorias (
            id_categoria INTEGER PRIMARY KEY,
            nombre VARCHAR(20) NOT NULL,
            pasillo INTEGER
        );
    """
)

#Se crea la tabla productos con forekey de categorias
cursor.execute (
    """ CREATE TABLE IF NOT EXISTS Productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_categoria INTEGER,
            codigo TEXT UNIQUE NOT NULL,
            nombre VARCHAR(20) NOT NULL,
            descripcion VARCHAR(40),
            precio FLOAT NOT NULL,
            fOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria)
        );
    """
)

#Se crea la tabla usuarios definiendo dos roles admin empleado
cursor.execute (
    """ CREATE TABLE IF NOT EXISTS Usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            rol TEXT CHECK(rol IN ('admin', 'empleado')) NOT NULL
        );
    """
)

#se crea la tabla movimientos usando forekey de usuarios y productos
cursor.execute (
    """ CREATE TABLE IF NOT EXISTS Movimientos (
            id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            tipo TEXT CHECK(tipo IN ('entrada', 'salida', 'ajuste', 'inicial')) NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha_registro DATE DEFAULT (date('now')),
            FOREIGN KEY (id_producto) REFERENCES Productos(id_producto),
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
        );
    """
)

#
cursor.execute (
    """ CREATE TABLE IF NOT EXISTS Stock (
            id_stock INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER UNIQUE NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
        );
    """
)

#crear por defecto un usuario admin al crear la DB
#cursor.execute(
#    """
#        INSERT INTO usuarios (usuario, password, rol)
#        VALUES (?, ?, ?)
#    """, 
#    ("admin", "1234", "admin"))

categorias = [
    "Abarrotes",
    "Bebidas",
    "Lácteos",
    "Snacks y Dulces",
    "Panadería",
    "Frutas y Verduras",
    "Carnes y Embutidos",
    "Limpieza y Aseo",
    "Cuidado Personal",
    "Otros"
]

for cat in categorias:
        cursor.execute("SELECT * FROM categorias WHERE nombre = ?", (cat,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (cat,))



print("Base de datos creada con exito")

conn.commit()
conn.close()


# Si la tabla Usuarios está vacía, insertar un usuario admin por defecto
