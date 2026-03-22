from utilidades import obtener_opcion
from registrar import registrar_producto
from visualizar import visualizar_productos
from actualizar import actualizar_producto
from eliminar import eliminar_producto
from buscar import menu_busqueda
from reporte import reporte_stock_bajo

from colorama import Fore, Style, init
init(autoreset=True)

def menu():
    """
    Menú principal del sistema de inventario.
    """
    while True:
        print(f"\n{Fore.CYAN}--- MENÚ PRINCIPAL DEL INVENTARIO ---{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Registrar producto")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Visualizar productos")
        print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Actualizar producto por ID")
        print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Eliminar producto por ID")
        print(f"{Fore.YELLOW}5.{Style.RESET_ALL} Buscar productos (ID, Nombre, Marca)")
        print(f"{Fore.YELLOW}6.{Style.RESET_ALL} Reporte de stock bajo")
        print(f"{Fore.YELLOW}7.{Style.RESET_ALL} Salir")

        opcion = obtener_opcion()

        if opcion == 1:
            registrar_producto()
        elif opcion == 2:
            visualizar_productos()
        elif opcion == 3:
            actualizar_producto()
        elif opcion == 4:
            eliminar_producto()
        elif opcion == 5:
            menu_busqueda()
        elif opcion == 6:
            reporte_stock_bajo()
        elif opcion == 7:
            print(f"{Fore.MAGENTA}Saliendo del sistema... ¡Vuelva pronto!{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    menu()
