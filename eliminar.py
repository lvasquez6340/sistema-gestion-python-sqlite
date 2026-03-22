from colorama import Fore, Style, init
from conexionbd import conectar
init(autoreset=True)

def eliminar_producto():
    """
    Permite eliminar un producto del inventario solicitando su ID.
    Muestra los datos actuales antes de confirmar la eliminación.
    """
    conn, cursor = conectar()

    print(f"{Fore.CYAN}--- ELIMINAR PRODUCTO ---{Style.RESET_ALL}")

    id_producto = input("Ingrese el ID del producto que desea eliminar: ").strip()
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

    nombre, descripcion, cantidad, precio, marca, categoria = prod

    print(f"\n{Fore.YELLOW}Datos del producto a eliminar:{Style.RESET_ALL}")
    print(f"Nombre: {nombre}")
    print(f"Descripción: {descripcion}")
    print(f"Cantidad: {cantidad}")
    print(f"Precio: ${precio:.2f}")
    print(f"Marca: {marca if marca else 'Sin Marca'}")
    print(f"Categoría: {categoria if categoria else 'Sin Categoría'}\n")

    confirmacion = input(f"{Fore.RED}¿Está seguro que desea eliminar este producto? (s/n): {Style.RESET_ALL}").strip().lower()
    if confirmacion != 's':
        print(f"{Fore.GREEN}Operación cancelada. El producto no fue eliminado.{Style.RESET_ALL}")
        conn.close()
        return

    try:
        cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
        conn.commit()
        print(f"{Fore.GREEN}Producto eliminado exitosamente.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error al eliminar el producto: {e}{Style.RESET_ALL}")
    finally:
        conn.close()
