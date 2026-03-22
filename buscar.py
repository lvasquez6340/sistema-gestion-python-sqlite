from colorama import Fore, Style, init
from conexionbd import conectar
init(autoreset=True)

def menu_busqueda():
    """
    Mini menú para buscar productos por ID, Nombre o Marca.
    """
    while True:
        print(f"\n{Fore.CYAN}--- MENÚ DE BÚSQUEDA ---{Style.RESET_ALL}")
        print("1. Buscar producto por ID")
        print("2. Buscar productos por Nombre")
        print("3. Buscar productos por Marca")
        print("4. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            buscar_producto_por_id()
        elif opcion == "2":
            buscar_productos_por_nombre()
        elif opcion == "3":
            buscar_productos_por_marca()
        elif opcion == "4":
            print(f"{Fore.GREEN}Volviendo al menú principal...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Opción inválida. Intente nuevamente.{Style.RESET_ALL}")

def buscar_producto_por_id():
    """
    Busca un producto por su ID y muestra todos los datos en el orden oficial.
    """
    conn, cursor = conectar()
    print(f"{Fore.CYAN}--- BUSCAR PRODUCTO POR ID ---{Style.RESET_ALL}")

    id_producto = input("Ingrese el ID del producto: ").strip()
    if not id_producto.isdigit():
        print(f"{Fore.RED}ID inválido. Debe ser un número entero.{Style.RESET_ALL}")
        conn.close()
        return

    id_producto = int(id_producto)
    cursor.execute("""
        SELECT p.nombre, p.descripcion, p.cantidad, p.precio,
               m.nombre AS marca, c.nombre AS categoria
        FROM productos p
        LEFT JOIN marcas m ON p.id_marca = m.id_marca
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE p.id_producto = ?
    """, (id_producto,))
    prod = cursor.fetchone()

    if prod:
        mostrar_producto(prod)
    else:
        print(f"{Fore.RED}No se encontró un producto con ese ID.{Style.RESET_ALL}")

    conn.close()

def buscar_productos_por_nombre():
    """
    Permite buscar productos que coincidan (parcialmente) con un nombre.
    """
    conn, cursor = conectar()
    print(f"{Fore.CYAN}--- BUSCAR PRODUCTOS POR NOMBRE ---{Style.RESET_ALL}")

    nombre_buscar = input("Ingrese parte o todo el nombre a buscar: ").strip()
    if not nombre_buscar:
        print(f"{Fore.RED}Debe ingresar al menos un carácter.{Style.RESET_ALL}")
        conn.close()
        return

    cursor.execute("""
        SELECT p.nombre, p.descripcion, p.cantidad, p.precio,
               m.nombre AS marca, c.nombre AS categoria
        FROM productos p
        LEFT JOIN marcas m ON p.id_marca = m.id_marca
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE p.nombre LIKE ?
    """, ('%' + nombre_buscar + '%',))

    productos = cursor.fetchall()
    mostrar_listado(productos)

    conn.close()

def buscar_productos_por_marca():
    """
    Lista las marcas y permite buscar productos asociados a una marca.
    """
    conn, cursor = conectar()
    print(f"{Fore.CYAN}--- BUSCAR PRODUCTOS POR MARCA ---{Style.RESET_ALL}")

    cursor.execute("SELECT id_marca, nombre FROM marcas")
    marcas = cursor.fetchall()

    if not marcas:
        print(f"{Fore.RED}No hay marcas registradas en el sistema.{Style.RESET_ALL}")
        conn.close()
        return

    print(f"{Fore.YELLOW}Marcas disponibles:{Style.RESET_ALL}")
    for id_marca, nombre in marcas:
        print(f"  ID {id_marca}: {nombre}")

    id_marca = input("Ingrese el ID de la marca para ver sus productos: ").strip()
    if not id_marca.isdigit() or int(id_marca) not in [m[0] for m in marcas]:
        print(f"{Fore.RED}ID de marca no válido.{Style.RESET_ALL}")
        conn.close()
        return

    id_marca = int(id_marca)
    cursor.execute("""
        SELECT p.nombre, p.descripcion, p.cantidad, p.precio,
               m.nombre AS marca, c.nombre AS categoria
        FROM productos p
        LEFT JOIN marcas m ON p.id_marca = m.id_marca
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE p.id_marca = ?
    """, (id_marca,))

    productos = cursor.fetchall()
    mostrar_listado(productos)

    conn.close()

def mostrar_producto(prod):
    """
    Muestra un producto individual en el orden oficial.
    """
    nombre, descripcion, cantidad, precio, marca, categoria = prod
    descripcion = descripcion if descripcion else "Sin descripción"
    marca = marca if marca else "Sin Marca"
    categoria = categoria if categoria else "Sin Categoría"

    print(f"\n{Fore.YELLOW}Producto encontrado:{Style.RESET_ALL}")
    print(f"Nombre: {nombre}")
    print(f"Descripción: {descripcion}")
    print(f"Cantidad: {cantidad}")
    print(f"Precio: ${precio:.2f}")
    print(f"Marca: {marca}")
    print(f"Categoría: {categoria}")

def mostrar_listado(productos):
    """
    Muestra un listado de productos o un mensaje si no se encuentra ninguno.
    """
    if productos:
        print(f"\n{Fore.YELLOW}--- Productos encontrados ---{Style.RESET_ALL}")
        for prod in productos:
            mostrar_producto(prod)
            print("-" * 50)
    else:
        print(f"{Fore.RED}No se encontraron productos que coincidan con la búsqueda.{Style.RESET_ALL}")
