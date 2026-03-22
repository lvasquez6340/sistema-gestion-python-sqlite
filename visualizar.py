from colorama import Fore, Style, init
from conexion_bd import conectar
init(autoreset=True)

def visualizar_productos():
    """
    Muestra todos los productos registrados en el inventario,
    con nombre, descripción, precio, cantidad, nombre de la marca y nombre de la categoría.
    """
    conn, cursor = conectar()

    print(f"{Fore.CYAN}--- LISTADO DE PRODUCTOS ---{Style.RESET_ALL}")

    cursor.execute("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.cantidad, p.precio,
               m.nombre as marca, c.nombre as categoria
        FROM productos p
        LEFT JOIN marcas m ON p.id_marca = m.id_marca
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        ORDER BY p.id_producto;
    """)
    productos = cursor.fetchall()

    if productos:
        print(f"{Fore.YELLOW}ID | Nombre | Descripción | Cantidad | Precio | Marca | Categoría{Style.RESET_ALL}")
        print("-" * 100)
        for prod in productos:
            id_prod, nombre, descripcion, cantidad, precio, marca, categoria = prod
            marca = marca if marca else "Sin Marca"
            categoria = categoria if categoria else "Sin Categoría"
            descripcion = descripcion if descripcion else "Sin descripción"
            print(f"{id_prod} | {nombre} | {descripcion} | {cantidad} | ${precio:.2f} | {marca} | {categoria}")
    else:
        print(f"{Fore.RED}No hay productos registrados en el inventario.{Style.RESET_ALL}")

    conn.close()
