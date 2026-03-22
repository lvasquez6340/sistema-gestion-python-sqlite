from colorama import Fore, Style, init
from conexionbd import conectar
init(autoreset=True)

def reporte_stock_bajo():
    """
    Genera un reporte mostrando todos los productos cuya cantidad
    sea igual o inferior a un límite especificado por el usuario o usuaria,
    mostrando los datos en el orden oficial:
    nombre, descripción, cantidad, precio, marca y categoría.
    """
    conn, cursor = conectar()

    print(f"{Fore.CYAN}--- REPORTE DE STOCK BAJO ---{Style.RESET_ALL}")

    while True:
        limite = input("Ingrese el límite máximo de cantidad para el reporte: ").strip()
        if limite.isdigit():
            limite = int(limite)
            break
        else:
            print(f"{Fore.RED}Debe ingresar un número entero válido.{Style.RESET_ALL}")

    cursor.execute("""
        SELECT p.nombre, p.descripcion, p.cantidad, p.precio,
               m.nombre AS marca, c.nombre AS categoria
        FROM productos p
        LEFT JOIN marcas m ON p.id_marca = m.id_marca
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE p.cantidad <= ?
        ORDER BY p.cantidad ASC
    """, (limite,))
    productos = cursor.fetchall()

    if productos:
        print(f"\n{Fore.YELLOW}--- Productos con cantidad <= {limite} ---{Style.RESET_ALL}")
        for prod in productos:
            nombre, descripcion, cantidad, precio, marca, categoria = prod
            descripcion = descripcion if descripcion else "Sin descripción"
            marca = marca if marca else "Sin Marca"
            categoria = categoria if categoria else "Sin Categoría"

            print(f"Nombre: {nombre}")
            print(f"Descripción: {descripcion}")
            print(f"Cantidad: {cantidad}")
            print(f"Precio: ${precio:.2f}")
            print(f"Marca: {marca}")
            print(f"Categoría: {categoria}")
            print("-" * 50)
    else:
        print(f"{Fore.GREEN}No hay productos con cantidad igual o inferior a {limite}.{Style.RESET_ALL}")

    conn.close()
