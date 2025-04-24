from src.persistencia import guardar_valores, leer_valores
from src.visualizacion import generar_visualizacion_avl
from src.avl import AVL # Importa la clase AVL para crear el árbol
import sys # Para salir del programa

def mostrar_menu():
    """Muestra el menú de opciones al usuario."""
    print("\n¿Qué deseas hacer?")
    print("1. Introducir valores a mi árbol AVL.")
    print("2. Modificar los valores de mi árbol AVL.")
    print("3. Ver la imagen de mi árbol AVL.")
    print("4. Salir.")

def solicitar_valores():
    """Solicita al usuario una lista de números separados por coma."""
    while True:
        try:
            entrada = input("Introduce los elementos separados por comas (ej: 10, 5, 15): ")
            if not entrada: # Permite terminar con Enter vacío si se desea
                 print("Entrada vacía detectada.")
                 return []
            # Limpia espacios y divide por coma
            valores_str = [val.strip() for val in entrada.split(',')]
            # Intenta convertir a entero, maneja error si no es posible
            valores_int = [int(val) for val in valores_str if val] # Ignora strings vacíos si hay comas extra
            if not valores_int and entrada: # Si después de procesar no hay números pero sí hubo entrada
                print("Error: No se ingresaron números válidos. Intenta de nuevo.")
                continue
            return valores_int
        except ValueError:
            print("Error: Asegúrate de introducir solo números enteros separados por comas.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

def opcion_introducir_valores():
    """
    Maneja la opción 1: Introducir nuevos valores y guardarlos.
    Sobrescribe el archivo existente.
    """
    print("\n--- Introducir Valores ---")
    valores = solicitar_valores()
    if valores: # Solo guarda si se introdujeron valores
        if guardar_valores(valores): # Llama a la función de persistencia
            # Mensaje de confirmación según PRD/PDF
            print("Tus valores han sido guardados con éxito.")
        else:
            print("No se pudieron guardar los valores.")
    elif valores == []: # Si solicitar_valores devolvió lista vacía por entrada vacía
        print("No se introdujeron valores para guardar.")


def opcion_modificar_valores():
    """
    Maneja la opción 2: Modificar los valores existentes (reemplazarlos).
    Sobrescribe el archivo existente.
    """
    print("\n--- Modificar Valores ---")
    print("Introduce los *nuevos* valores que reemplazarán a los anteriores.")
    valores = solicitar_valores()
    if valores: # Solo guarda si se introdujeron valores
        if guardar_valores(valores): # Llama a la función de persistencia (sobrescribe)
             # Mensaje de confirmación según PRD/PDF
            print("Tus valores han sido modificados con éxito.")
        else:
            print("No se pudieron modificar los valores.")
    elif valores == []: # Si solicitar_valores devolvió lista vacía por entrada vacía
        print("No se introdujeron valores para modificar.")


def opcion_visualizar_arbol():
    """
    Maneja la opción 3: Visualizar el árbol.
    """
    print("\n--- Visualizar Árbol ---")
    nombre_archivo = input("Introduce el nombre de tu archivo (ej: Arboles.txt): ")
    if not nombre_archivo:
        nombre_archivo = "Arboles.txt" # Valor por defecto si no se ingresa nada

    print(f"Intentando leer valores de '{nombre_archivo}'...")
    valores = leer_valores(nombre_archivo)

    if valores is None:
        print("No se pudo leer el archivo o no contiene valores válidos.")
        return
    elif not valores:
        print("El archivo está vacío o no contiene números después del prefijo.")
        return

    print(f"Valores leídos: {valores}")

    #Crea el árbol AVL y lo visualiza
    print("Construyendo el árbol AVL...")
    arbol = AVL()
    raiz = None
    for valor in valores:
        raiz = arbol.insertar(raiz, valor)
    print("Generando visualización del árbol...")
    nombre_archivo_salida = input("Introduce el nombre del archivo de salida (sin extensión): ")
    if not nombre_archivo_salida:
        nombre_archivo = nombre_archivo.split('.')[0] # Extrae el nombre sin extensión
        nombre_archivo_salida = nombre_archivo # Valor por defecto si no se ingresa nada
    generar_visualizacion_avl(raiz, nombre_archivo_salida)


def main():
    """Función principal que ejecuta el menú."""
    # Mensaje de bienvenida según PDF
    print("Bienvenido al programa de Árboles AVL.")

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-4): ")

        if opcion == '1':
            opcion_introducir_valores()
        elif opcion == '2':
            opcion_modificar_valores()
        elif opcion == '3':
            opcion_visualizar_arbol()
        elif opcion == '4':
            # Mensaje de despedida según PDF
            print("\nHasta luego.")
            sys.exit() # Termina el programa
        else:
            print("Opción no válida. Por favor, introduce un número entre 1 y 4.")

if __name__ == "__main__":
    main()