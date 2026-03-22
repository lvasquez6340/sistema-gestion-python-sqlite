from colorama import Fore, Style, init
from conexion_bd import conectar
init(autoreset=True)

def actualizar_producto():
    """
    Permite actualizar un producto existente pidiendo su ID,
    mostrando los datos actuales en el orden oficial, y 
    solicitando los nuevos valores al usuario (opcional).
    """
    conn, cursor = conectar()

    print(f"{Fore.CYAN}--- ACTUALIZAR PRODUCTO ---{Style.RESET_ALL}")

    id_producto = input("Ingrese el ID del producto que desea actualizar: ").strip()
    if not id_producto.isdigit():
        print(f"{Fore.RED}ID inválido. Debe ser un número entero.{Style.RESET_ALL}")
        conn.close()
        return

    id_producto = int(id_producto)

    # Consultar datos actuales
    cursor.execute("""
        SELECT p.nombre, p.descripcion, p.cantidad, p.precio,
               m.nombre as marca, c.nombre as categoria
        FROM productos p
        LEFT JOIN marcas m ON p.id_marca = m.id_marca
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE p.id_producto = ?
    """, (id_producto,))
    prod = cursor.fetchone()

    if not prod:
        print(f"{Fore.RED}No se encontró un producto con ese ID.{Style.RESET_ALL}")
        conn.close()
        return

    nombre_actual, descripcion_actual, cantidad_actual, precio_actual, marca_actual, categoria_actual = prod

    print(f"\n{Fore.YELLOW}Datos actuales:{Style.RESET_ALL}")
    print(f"Nombre: {nombre_actual}")
    print(f"Descripción: {descripcion_actual}")
    print(f"Cantidad: {cantidad_actual}")
    print(f"Precio: ${precio_actual:.2f}")
    print(f"Marca: {marca_actual if marca_actual else 'Sin Marca'}")
    print(f"Categoría: {categoria_actual if categoria_actual else 'Sin Categoría'}\n")

    # Pedir nuevos valores
    nuevo_nombre = input(f"Nuevo nombre (Enter para mantener '{nombre_actual}'): ").strip() or nombre_actual
    nueva_descripcion = input(f"Nueva descripción (Enter para mantener '{descripcion_actual}'): ").strip() or descripcion_actual

    while True:
        nueva_cantidad = input(f"Nueva cantidad (Enter para mantener {cantidad_actual}): ").strip()
        if nueva_cantidad == "":
            nueva_cantidad = cantidad_actual
            break
        elif nueva_cantidad.isdigit():
            nueva_cantidad = int(nueva_cantidad)
            break
        else:
            print(f"{Fore.RED}Ingrese un número entero válido para cantidad.{Style.RESET_ALL}")

    while True:
        nuevo_precio = input(f"Nuevo precio (Enter para mantener {precio_actual}): ").strip()
        if nuevo_precio == "":
            nuevo_precio = precio_actual
            break
        try:
            nuevo_precio = float(nuevo_precio)
            break
        except ValueError:
            print(f"{Fore.RED}Ingrese un número válido para precio.{Style.RESET_ALL}")

    # Listar marcas
    cursor.execute("SELECT id_marca, nombre FROM marcas")
    marcas = cursor.fetchall()
    if marcas:
        print(f"{Fore.YELLOW}Marcas disponibles:{Style.RESET_ALL}")
        for id_marca, nombre_marca in marcas:
            print(f"  ID {id_marca}: {nombre_marca}")
    else:
        print(f"{Fore.RED}No hay marcas registradas.{Style.RESET_ALL}")

    id_marca = None
    while True:
        id_input = input(f"Ingrese ID de la nueva marca (Enter para mantener '{marca_actual}'): ").strip()
        if id_input == "":
            break
        elif id_input.isdigit() and int(id_input) in [m[0] for m in marcas]:
            id_marca = int(id_input)
            break
        else:
            print(f"{Fore.RED}ID de marca no válido. Intente nuevamente.{Style.RESET_ALL}")

    # Listar categorías
    cursor.execute("SELECT id_categoria, nombre FROM categorias")
    categorias = cursor.fetchall()
    if categorias:
        print(f"{Fore.YELLOW}Categorías disponibles:{Style.RESET_ALL}")
        for id_cat, nombre_cat in categorias:
            print(f"  ID {id_cat}: {nombre_cat}")
    else:
        print(f"{Fore.RED}No hay categorías registradas.{Style.RESET_ALL}")

    id_categoria = None
    while True:
        id_input = input(f"Ingrese ID de la nueva categoría (Enter para mantener '{categoria_actual}'): ").strip()
        if id_input == "":
            break
        elif id_input.isdigit() and int(id_input) in [c[0] for c in categorias]:
            id_categoria = int(id_input)
            break
        else:
            print(f"{Fore.RED}ID de categoría no válido. Intente nuevamente.{Style.RESET_ALL}")

    # ACTUALIZO EN LA TABLA
    try:
        cursor.execute("""
            UPDATE productos
            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, 
                id_marca = ?, id_categoria = ?
            WHERE id_producto = ?
        """, (nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, id_marca, id_categoria, id_producto))
        conn.commit()
        print(f"{Fore.GREEN}Producto actualizado exitosamente.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error al actualizar el producto: {e}{Style.RESET_ALL}")
    finally:
        conn.close()
