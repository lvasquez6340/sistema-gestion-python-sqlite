from colorama import Fore, Style, init
from conexion_bd import conectar
init(autoreset=True)

def registrar_producto():
    """
    Registra un producto permitiendo además crear nuevas marcas o categorías
    si el usuario así lo desea.
    """
    conn, cursor = conectar()

    print(f"{Fore.CYAN}--- REGISTRAR NUEVO PRODUCTO ---{Style.RESET_ALL}")

    # ----------------------------------------------------
    # MANEJO DE MARCAS
    # ----------------------------------------------------
    cursor.execute("SELECT id_marca, nombre FROM marcas")
    marcas = cursor.fetchall()

    if marcas:
        print(f"{Fore.YELLOW}Marcas disponibles:{Style.RESET_ALL}")
        for id_marca, nombre_marca in marcas:
            print(f"  ID {id_marca}: {nombre_marca}")
    else:
        print(f"{Fore.RED}No hay marcas registradas.{Style.RESET_ALL}")

    # Preguntar si quiere agregar una nueva marca
    opcion_marca = input("¿Desea crear una nueva marca? (s/n): ").strip().lower()
    if opcion_marca == 's':
        nueva_marca = input("Ingrese el nombre de la nueva marca: ").strip()
        if nueva_marca:
            cursor.execute("INSERT INTO marcas (nombre) VALUES (?)", (nueva_marca,))
            conn.commit()
            print(f"{Fore.GREEN}Marca '{nueva_marca}' creada exitosamente.{Style.RESET_ALL}")
            cursor.execute("SELECT id_marca, nombre FROM marcas")
            marcas = cursor.fetchall()

    # ----------------------------------------------------
    # MANEJO DE CATEGORÍAS
    # ----------------------------------------------------
    cursor.execute("SELECT id_categoria, nombre FROM categorias")
    categorias = cursor.fetchall()

    if categorias:
        print(f"{Fore.YELLOW}Categorías disponibles:{Style.RESET_ALL}")
        for id_cat, nombre_cat in categorias:
            print(f"  ID {id_cat}: {nombre_cat}")
    else:
        print(f"{Fore.RED}No hay categorías registradas.{Style.RESET_ALL}")

    opcion_categoria = input("¿Desea crear una nueva categoría? (s/n): ").strip().lower()
    if opcion_categoria == 's':
        nueva_categoria = input("Ingrese el nombre de la nueva categoría: ").strip()
        if nueva_categoria:
            cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nueva_categoria,))
            conn.commit()
            print(f"{Fore.GREEN}Categoría '{nueva_categoria}' creada exitosamente.{Style.RESET_ALL}")
            cursor.execute("SELECT id_categoria, nombre FROM categorias")
            categorias = cursor.fetchall()

    # ----------------------------------------------------
    # DATOS DEL PRODUCTO
    # ----------------------------------------------------
    # NOMBRE
    while True:
        nombre = input("Nombre del producto: ").strip()
        if nombre:
            break
        print(f"{Fore.RED}El nombre no puede estar vacío.{Style.RESET_ALL}")
    # DESCRIPCION
    while True:
        descripcion = input("Descripcion del producto: ").strip()
        if nombre:
            break
        print(f"{Fore.RED}La descripción no puede estar vacío.{Style.RESET_ALL}")
    # CANTIDAD
    while True:
        cantidad = input("Cantidad inicial en stock: ").strip()
        if cantidad.isdigit():
            cantidad = int(cantidad)
            break
        else:
            print(f"{Fore.RED}Ingrese un número entero válido para la cantidad.{Style.RESET_ALL}")
    # PRECIO
    while True:
        precio = input("Precio del producto: ").strip()
        try:
            precio = float(precio)
            if precio < 0:
                print(f"{Fore.RED}El precio no puede ser negativo.{Style.RESET_ALL}")
            else:
                break
        except ValueError:
            print(f"{Fore.RED}Ingrese un número válido para el precio.{Style.RESET_ALL}")

    # ----------------------------------------------------
    # SELECCIÓN DE ID MARCA Y CATEGORÍA
    # ----------------------------------------------------
    id_marca = None
    if marcas:
        while True:
            id_input = input("Ingrese el ID de la marca (opcional, Enter para NULL): ").strip()
            if id_input == "":
                break
            elif id_input.isdigit() and int(id_input) in [m[0] for m in marcas]:
                id_marca = int(id_input)
                break
            else:
                print(f"{Fore.RED}ID de marca no válido. Intente nuevamente.{Style.RESET_ALL}")

    id_categoria = None
    if categorias:
        while True:
            id_input = input("Ingrese el ID de la categoría (opcional, Enter para NULL): ").strip()
            if id_input == "":
                break
            elif id_input.isdigit() and int(id_input) in [c[0] for c in categorias]:
                id_categoria = int(id_input)
                break
            else:
                print(f"{Fore.RED}ID de categoría no válido. Intente nuevamente.{Style.RESET_ALL}")

    # ----------------------------------------------------
    # INSERTAR EL PRODUCTO
    # ----------------------------------------------------
    try:
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, cantidad, precio, id_marca, id_categoria)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, descripcion, cantidad, precio, id_marca, id_categoria))
        conn.commit()
        print(f"{Fore.GREEN}Producto registrado exitosamente.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error al registrar el producto: {e}{Style.RESET_ALL}")
    finally:
        conn.close()

