import sqlite3 as sql

if __name__=="__main__":
    
    #conn es un objeto que permite la conexion con la DB
    conn = sql.connect("inventario.db")
    cursor = conn.cursor()

    #Se crea la tabla categorias
    cursor.execute (
        """ CREATE TABLE IF NOT EXISTS Categorias (
                id_categoria INTEGER PRYMARY KEY AUTOINCREMENT,
                nombre VARCHAR(20) NOT NULL,
                pasillo INTEGER
            );
        """
    )
    
    #Se crea la tabla productos con forekey de categorias
    cursor.execute (
        """ CREATE TABLE IF NOT EXIST Productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                id_categoria INTEGER,
                codigo INTEGER UNIQUE NOT NULL,
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
                tipo TEXT CHECK(tipo IN ('entrada', 'salida')) NOT NULL,
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