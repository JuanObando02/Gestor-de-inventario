import sqlite3 as sql
import os, sys
from src.utils.path_utils import resource_path

db_path = resource_path(os.path.join("data", "inventario.db"))

def get_connection():
    return sql.connect(db_path, timeout=10)

# Obtener todas las categorías
def get_all_categorias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_categoria, nombre FROM Categorias")
    categorias = cur.fetchall()  # devuelve lista de tuplas [(1, 'Bebidas'), (2, 'Lácteos'), ...]
    conn.close()
    return categorias

def add_categoria(nombre):
    """Agrega una nueva categoría y devuelve su id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Categorias (nombre) VALUES (?)", (nombre,))
    conn.commit()
    id_cat = cur.lastrowid
    conn.close()
    return id_cat


def update_categoria(id_categoria, nuevo_nombre):
    """Actualiza el nombre de una categoría existente."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Categorias SET nombre = ? WHERE id_categoria = ?",
        (nuevo_nombre, id_categoria)
    )
    conn.commit()
    conn.close()


def delete_categoria(id_categoria):
    """Elimina una categoría (solo si no tiene productos asociados)."""
    conn = get_connection()
    cur = conn.cursor()

    # Verificar si está en uso
    cur.execute("SELECT COUNT(*) FROM Productos WHERE id_categoria = ?", (id_categoria,))
    count = cur.fetchone()[0]
    if count > 0:
        conn.close()
        raise ValueError("No se puede eliminar la categoría porque tiene productos asociados.")

    cur.execute("DELETE FROM Categorias WHERE id_categoria = ?", (id_categoria,))
    conn.commit()
    conn.close()