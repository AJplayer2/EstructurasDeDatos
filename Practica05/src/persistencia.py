import os

def guardar_valores(valores, nombre_archivo="Arboles.txt"):
    """
    Guarda la secuencia de números en el archivo especificado,
    sobrescribiendo el archivo si ya existe.

    Args:
        valores (list): Lista de números (enteros) a guardar.
        nombre_archivo (str): Nombre del archivo donde se guardarán los valores.
                              Por defecto es "Arboles.txt".
    """
    try:
        # Convierte los números a string y los une con ", "
        valores_str = ", ".join(map(str, valores))
        # Crea la línea con el formato requerido
        linea = f"Arbol AVL: {valores_str}"

        # Abre el archivo en modo escritura ('w'), lo que crea el archivo
        # si no existe, o lo sobrescribe si existe.
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(linea + '\n') # Agrega un salto de línea al final
        print(f"Valores guardados con éxito en '{nombre_archivo}'.")
        return True
    except IOError as e:
        print(f"Error al guardar el archivo '{nombre_archivo}': {e}")
        return False
    except Exception as e:
        print(f"Ocurrió un error inesperado al guardar: {e}")
        return False

def leer_valores(nombre_archivo="Arboles.txt"):
    """
    Lee la secuencia de números desde el archivo especificado.

    Args:
        nombre_archivo (str): Nombre del archivo desde donde se leerán los valores.
                              Por defecto es "Arboles.txt".

    Returns:
        list: Una lista de números enteros leídos del archivo,
              o None si el archivo no existe o hay un error.
    """
    if not os.path.exists(nombre_archivo):
        print(f"Error: El archivo '{nombre_archivo}' no existe.")
        return None

    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            linea = f.readline().strip() # Lee la primera línea y quita espacios/saltos

        # Verifica si la línea tiene el prefijo esperado
        prefijo = "Arbol AVL:"
        if not linea.startswith(prefijo):
            print(f"Error: Formato incorrecto en el archivo '{nombre_archivo}'.")
            print(f"Se esperaba que comenzara con '{prefijo}'.")
            return None

        # Extrae la parte de los números después del prefijo
        valores_str = linea[len(prefijo):]

        # Si no hay números después del prefijo, retorna lista vacía
        if not valores_str:
            return []

        # Separa los números por coma y espacio, y convierte a entero
        try:
            valores = [int(val.strip()) for val in valores_str.split(',')]
            print(f"Valores leídos con éxito desde '{nombre_archivo}'.")
            return valores
        except ValueError:
            print(f"Error: No se pudieron convertir todos los valores a números enteros en '{nombre_archivo}'.")
            print(f"Valores leídos: '{valores_str}'")
            return None

    except IOError as e:
        print(f"Error al leer el archivo '{nombre_archivo}': {e}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado al leer: {e}")
        return None

# Ejemplo de uso:
if __name__ == "__main__":
    # Ejemplo 1: Guardar valores nuevos (creará o sobrescribirá Arboles.txt)
    valores_nuevos = [12, 15, 30, 67, 3]
    print(f"\nIntentando guardar: {valores_nuevos}")
    guardar_valores(valores_nuevos)

    # Ejemplo 2: Leer los valores guardados
    print("\nIntentando leer valores...")
    valores_leidos = leer_valores()
    if valores_leidos is not None:
        print(f"Valores leídos: {valores_leidos}")

    # Ejemplo 3: Modificar valores (sobrescribir Arboles.txt)
    valores_modificados = [30, 20, 40, 10, 25, 5, 15, 27, 35, 50, 1]
    print(f"\nIntentando modificar/guardar: {valores_modificados}")
    guardar_valores(valores_modificados)

    # Ejemplo 4: Leer los valores modificados
    print("\nIntentando leer valores modificados...")
    valores_leidos_mod = leer_valores()
    if valores_leidos_mod is not None:
        print(f"Valores leídos: {valores_leidos_mod}")

    # Ejemplo 5: Intentar leer un archivo que no existe
    print("\nIntentando leer un archivo inexistente...")
    leer_valores("archivo_no_existe.txt")

    # Ejemplo 6: Guardar una lista vacía
    print("\nIntentando guardar una lista vacía...")
    guardar_valores([])
    valores_vacios = leer_valores()
    if valores_vacios is not None:
        print(f"Valores leídos (lista vacía): {valores_vacios}")

    # Ejemplo 7: Crear un archivo con formato incorrecto y leerlo
    print("\nCreando archivo con formato incorrecto...")
    try:
        with open("formato_incorrecto.txt", "w") as f:
            f.write("Valores: 1, 2, 3")
        print("Intentando leer archivo con formato incorrecto...")
        leer_valores("formato_incorrecto.txt")
    except Exception as e:
        print(f"Error creando archivo de prueba: {e}")