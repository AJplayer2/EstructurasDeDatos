# Práctica 5: Árboles Binarios AVL - Estructuras de Datos

Este proyecto implementa un Árbol Binario de Búsqueda Auto-Balanceable (AVL) desde cero en Python, como parte de la Práctica 5 del curso de Estructuras de Datos. Permite al usuario interactuar a través de una interfaz de línea de comandos (CLI) para introducir, modificar y visualizar los elementos del árbol. La visualización se genera utilizando la biblioteca Graphviz.

## Funcionalidades

El programa ofrece un menú interactivo en la consola con las siguientes opciones [cite: Práctica5.pdf, PRD.md]:

1.  **Introducir valores a mi árbol AVL:**
    * Permite al usuario ingresar una secuencia de números enteros separados por comas.
    * Estos números se guardan en el archivo `Arboles.txt`, sobrescribiéndolo si ya existe.
    * El formato en el archivo es: `Arbol AVL: num1, num2, num3,...`
2.  **Modificar los valores de mi árbol AVL:**
    * Permite al usuario ingresar una *nueva* secuencia de números enteros separados por comas.
    * Esta nueva secuencia reemplaza completamente el contenido anterior del archivo `Arboles.txt`.
3.  **Ver la imagen de mi árbol AVL:**
    * Solicita el nombre del archivo que contiene los datos (por defecto `Arboles.txt`).
    * Lee la secuencia de números del archivo.
    * Construye un árbol AVL en memoria insertando los números en el orden en que aparecen en el archivo.
    * Genera una imagen (`.png`) del árbol AVL resultante utilizando Graphviz.
    * Intenta abrir automáticamente la imagen generada.
4.  **Salir:**
    * Termina la ejecución del programa.

## Requisitos

* **Python:** Versión 3.12 o superior.
* **Biblioteca `graphviz` de Python:** Necesaria para generar la visualización.
* **Software Graphviz:** El motor de renderizado gráfico debe estar instalado en el sistema operativo y, preferiblemente, añadido al PATH del sistema.

## Instalación

1.  **Crear y activar un entorno virtual (Recomendado):**
    ```bash
    python -m venv .env
    # En Windows
    .\.env\Scripts\activate
    # En macOS/Linux
    source .env/bin/activate
    ```

2.  **Instalar la biblioteca `graphviz` de Python:**
    ```bash
    pip install graphviz
    ```

3.  **Instalar el software Graphviz:**
    * Descarga e instala Graphviz desde el sitio oficial: [https://graphviz.org/download/](https://graphviz.org/download/)
    * **Importante:** Durante la instalación (o después), asegúrate de que la opción para añadir Graphviz al PATH del sistema esté seleccionada. Si no, podrías necesitar añadir manualmente el directorio `bin` de Graphviz a tu variable de entorno `PATH` o especificar la ruta en el archivo `main.py`.

## Uso

1.  Activa tu entorno virtual (si creaste uno).
2.  Ejecuta el script principal desde la terminal:
    ```bash
    python main.py
    ```
3.  Sigue las instrucciones presentadas en el menú interactivo.
    * Introduce los números separados por comas cuando se te solicite.
    * El archivo `Arboles.txt` se creará o modificará en el mismo directorio.
    * Al visualizar, se generará un archivo de imagen y el programa intentará abrirlo con el visor de imágenes predeterminado.

## Estructura de Archivos

* `main.py`: Contiene la lógica principal de la aplicación, la interfaz de línea de comandos (CLI) y coordina las llamadas a otros módulos.
* `avl.py`: Define las clases `Nodo` y `AVL`, implementando la estructura de datos del árbol AVL y sus operaciones de inserción y autobalanceo (rotaciones).
* `persistencia.py`: Contiene las funciones `guardar_valores` y `leer_valores` para manejar la lectura y escritura del archivo `Arboles.txt`.
* `visualizacion.py`: Contiene la función `generar_visualizacion_avl` que utiliza la biblioteca `graphviz` para crear y mostrar la imagen del árbol.
* `Arboles.txt`: Archivo de texto generado por el programa para almacenar la secuencia de números del árbol (se crea/modifica al usar las opciones 1 o 2).
* `*.png`: Archivos de imagen generados al usar la opción 3 (el nombre base suele coincidir con el del archivo de datos, ej: `Arboles.png`).

## Punto Extra

La visualización generada cumple con los requisitos del punto extra:
* Los nodos del árbol se muestran como círculos (`shape='circle'`).
* Los nodos tienen un color de relleno personalizado (`fillcolor='lightblue'`).

