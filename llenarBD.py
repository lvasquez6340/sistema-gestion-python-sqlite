import sqlite3
from colorama import Fore, Style, init
init(autoreset=True)

def poblar_db():
    """
    Inserta datos en las tablas marcas, categorias y productos.
    """
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    try:
        # Insertar marcas
        cursor.executemany("INSERT INTO marcas (nombre) VALUES (?)", [
            ('Coca-Cola',),
            ('Pepsi',),
            ('La Serenísima',),
            ('Sancor',),
            ('Unilever',),
            ('Molinos Río',),
            ('Nestlé',),
            ('Colgate-Palmolive',)
        ])
        
        # Insertar categorías
        cursor.executemany("INSERT INTO categorias (nombre) VALUES (?)", [
            ('Bebidas',),
            ('Lácteos',),
            ('Higiene',),
            ('Alimentos',)
        ])

        # Insertar productos
        cursor.executemany("""
            INSERT INTO productos (nombre, descripcion, cantidad, precio, id_marca, id_categoria)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ('Coca-Cola Zero', 'Botella 1.5L sin azúcar', 20, 850.00, 1, 1),
            ('Pepsi Light', 'Botella 2L sin azúcar', 15, 790.00, 2, 1),
            ('Leche Entera', 'Pack x12 de 1L', 10, 650.00, 3, 2),
            ('Yogur Vainilla', 'Pack x4 potes', 25, 450.00, 4, 2),
            ('Shampoo Dove', 'Botella 400ml hidratante', 12, 1200.00, 5, 3),
            ('Arroz Largo Fino', 'Bolsa 1kg', 50, 320.00, 6, 4),
            ('Café Nescafé', 'Frasco 170g instantáneo', 8, 1800.00, 7, 4),
            ('Jabón Protex', 'Barra antibacterial x90g', 40, 220.00, 8, 3)
        ])

        conn.commit()
        print(f"{Fore.GREEN}Base de datos poblada exitosamente.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error al poblar la base de datos: {e}{Style.RESET_ALL}")
    finally:
        conn.close()

if __name__ == "__main__":
    poblar_db()
