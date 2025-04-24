import graphviz
import os

if __name__ == "__main__": #Para evitar errores de importación al ejecutar el script directamente
    from avl import AVL # Necesitamos AVL para construir un árbol de ejemplo

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

def _agregar_nodos_y_aristas(nodo, dot):
    """
    Función auxiliar recursiva para agregar nodos y aristas al objeto Digraph.
    También aplica el estilo para el punto extra.
    """
    if nodo is None:
        return

    #Le damos forma a los nodos
    dot.node(
        name=str(id(nodo)),
        label=str(nodo.valor),
        shape='circle',
        fillcolor='lightblue',
        style='filled'
    )

    # Agregar arista desde el padre (si existe) al hijo izquierdo
    if nodo.hijo_izquierdo:
        # Asegurarse de que el nombre del nodo hijo también se agregue antes de crear la arista
        _agregar_nodos_y_aristas(nodo.hijo_izquierdo, dot)
        dot.edge(str(id(nodo)), str(id(nodo.hijo_izquierdo)))


    # Agregar arista desde el padre (si existe) al hijo derecho
    if nodo.hijo_derecho:
         # Asegurarse de que el nombre del nodo hijo también se agregue antes de crear la arista
        _agregar_nodos_y_aristas(nodo.hijo_derecho, dot)
        dot.edge(str(id(nodo)), str(id(nodo.hijo_derecho)))

def generar_visualizacion_avl(raiz_nodo, nombre_archivo_salida="arbol_avl_img"):
    """
    Genera una visualización del árbol AVL usando Graphviz.

    Args:
        raiz_nodo (Nodo): El nodo raíz del árbol AVL a visualizar.
        nombre_archivo_salida (str): El nombre base para el archivo de imagen
                                     (sin extensión). Se generará un .gv y un .png.
    """
    if raiz_nodo is None:
        print("El árbol está vacío, no se puede generar visualización.")
        return

    # Crear un nuevo grafo dirigido
    dot = graphviz.Digraph(comment='Árbol AVL')

    # Llenar el grafo recursivamente
    _agregar_nodos_y_aristas(raiz_nodo, dot)

    try:
        # Renderizar el grafo: genera archivo .gv y .gv.png (o el formato especificado)
        # view=True intenta abrir la imagen generada automáticamente
        # cleanup=True elimina el archivo .gv intermedio
        formato_imagen = 'png'
        archivo_renderizado = dot.render(nombre_archivo_salida, format=formato_imagen, view=True, cleanup=True)
        print(f"Visualización del árbol guardada como '{archivo_renderizado}' y abierta.")
        # Nota: El comportamiento de view=True puede depender del sistema operativo y visor de imágenes.

    except graphviz.backend.execute.ExecutableNotFound:
        print("\nError: No se encontró la instalación de Graphviz.")
        print(f"Se generó el archivo de definición: '{nombre_archivo_salida}.gv'")
    except Exception as e:
        print(f"\nOcurrió un error al generar o mostrar la visualización: {e}")
        print(f"Se generó el archivo de definición: '{nombre_archivo_salida}.gv'")


# Ejemplo de uso:
if __name__ == "__main__":
    # 1. Crear un árbol AVL de ejemplo
    arbol = AVL()
    raiz = None
    valores = [30, 20, 40, 10, 25, 5, 15, 27, 35, 50, 1] # Ejemplo

    print(f"Construyendo árbol AVL con valores: {valores}")
    for valor in valores:
        raiz = arbol.insertar(raiz, valor)

    print("\nÁrbol construido. Generando visualización...")

    # 2. Llamar a la función de visualización con la raíz del árbol
    generar_visualizacion_avl(raiz, nombre_archivo_salida="mi_arbol_avl")

    print("\n--- Ejemplo con árbol vacío ---")
    generar_visualizacion_avl(None)

    print("\n--- Ejemplo con árbol de un solo nodo ---")
    raiz_simple = arbol.insertar(None, 100)
    generar_visualizacion_avl(raiz_simple, nombre_archivo_salida="arbol_simple")