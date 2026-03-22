from colorama import init, Fore, Style
init(autoreset=True)

def obtener_opcion():
    """
    Solicita al usuario que ingrese una opción numérica del menú principal
    y valida que sea un número entre 1 y 8.

    Returns:
        int: opción elegida por el usuario
    """
    while True:
        opcion = input(f"{Fore.GREEN}Seleccione una opción (1-8): {Style.RESET_ALL}")
        if not opcion.strip():
            print(f"{Fore.RED}Entrada vacía. Ingrese un número.{Style.RESET_ALL}")
        elif not opcion.isdigit():
            print(f"{Fore.RED}Debe ingresar un número válido.{Style.RESET_ALL}")
        else:
            opcion_int = int(opcion)
            if 1 <= opcion_int <= 8:
                return opcion_int
            else:
                print(f"{Fore.RED}Número fuera de rango. Elija entre 1 y 8.{Style.RESET_ALL}")
