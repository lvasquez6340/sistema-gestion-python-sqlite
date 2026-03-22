import sqlite3

def conectar():
    """
    Abre la conexión a la base de datos y retorna (conn, cursor).
    """
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    # Crear tablas si no existen
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marcas (
        id_marca INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        id_marca INTEGER,
        id_categoria INTEGER,
        FOREIGN KEY (id_marca) REFERENCES marcas(id_marca),
        FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
    );
    """)
    conn.commit()
    return conn, cursor
