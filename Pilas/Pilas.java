import java.util.Scanner;

/**
 * La clase {@code Pilas} simula una estructura de datos tipo pila que almacena enteros.
 * <p>
 * La pila se implementa internamente como un arreglo que se redimensiona dinámicamente.
 * Se proporcionan métodos para agregar (apilar) y eliminar (desapilar) elementos,
 * permitiendo la interacción con la estructura a través de un menú en el método {@code main}.
 * <p>
 * <b>Uso:</b>
 * <ul>
 *   <li>Utilice {@code agregarElemento(int)} para agregar un elemento al tope de la pila.</li>
 *   <li>Utilice {@code eliminarElemento(int)} para eliminar uno o más elementos del tope.</li>
 *   <li>El método {@code toString()} devuelve una representación textual de la pila.</li>
 * </ul>
 * <p>
 * <b>Nota:</b> Solo se utilizan clases del paquete {@code java.util.Scanner} para la entrada
 * de datos, siguiendo las restricciones establecidas.
 *
 * @author Angel Jayden Maya Morales
 */
public class Pilas {

    /**
     * Arreglo que almacena los elementos de la pila.
     */
    private int[] pila;

    /**
     * Constructor que inicializa la pila vacía.
     */
    public Pilas() {
        pila = new int[0];
    }

    /**
     * Devuelve una representación en forma de cadena de la pila.
     * <p>
     * El método recorre todos los elementos de la pila (desde el tope hasta el fondo)
     * y los concatena en un solo {@code String} separado por espacios.
     *
     * @return una cadena que contiene los elementos actuales de la pila.
     */
    @Override
    public String toString() {
        String s = "";
        for (int elemento : pila) {
            s += elemento + " ";
        }
        return s.trim();
    }
 
    /**
     * Agrega un elemento al tope de la pila.
     * <p>
     * Este método crea un nuevo arreglo con un espacio adicional, desplaza los elementos
     * existentes una posición hacia abajo y coloca el nuevo elemento en la primera posición,
     * simulando el comportamiento de apilar.
     * <p>
     * Es especialmente útil en casos donde se necesita almacenar datos de forma temporal,
     * permitiendo operaciones posteriores de eliminación o retroceso.
     *
     * @param elemento el valor entero que se desea agregar a la pila.
     */
    public void agregarElemento(int elemento) {
        // Se crea un nuevo arreglo con un espacio adicional.
        int[] pilaTemp = new int[pila.length + 1];
        // Se copian los elementos existentes desplazándolos una posición.
        for (int i = 0; i < pila.length; i++) {
            pilaTemp[i + 1] = pila[i];
        }
        // Se asigna el nuevo elemento en la posición 0 (tope de la pila).
        pilaTemp[0] = elemento;
        pila = pilaTemp;
        System.out.println("Pila actual: " + this);
    }

    /**
     * Elimina una cantidad específica de elementos del tope de la pila.
     * <p>
     * Este método extrae y muestra los elementos eliminados desde el tope de la pila.
     * Si la cantidad solicitada es mayor que el número de elementos presentes, se muestra
     * un mensaje de error y no se realiza ninguna eliminación.
     * <p>
     * Es útil para revertir operaciones o limpiar la pila en situaciones donde se requiera
     * eliminar varios elementos de manera simultánea.
     *
     * @param cantidad el número de elementos que se desean eliminar del tope de la pila.
     */
    public void eliminarElemento(int cantidad) {
        // Verificar que la cantidad a eliminar no supere el número de elementos existentes.
        if (cantidad > pila.length) {
            System.out.println("Error: No hay suficientes elementos en la pila para eliminar " + cantidad + " elemento(s).");
            return;
        }

        // Mostrar los elementos que serán eliminados.
        if (cantidad == 1) {
            System.out.println("El elemento que sale es:");
        } else {
            System.out.println("Los elementos que salen son:");
        }
        for (int i = 0; i < cantidad; i++) {
            System.out.print(pila[pila.length-i-1] + " ");
        }
        System.out.println();

        // Crear un nuevo arreglo para almacenar los elementos restantes.
        int[] pilaTemp = new int[pila.length - cantidad];
        // Copiar los elementos restantes desde la posición 'cantidad' hasta el final del arreglo original.
        for (int i = pilaTemp.length; i > 0; i--) {
            pilaTemp[i-1] = pila[i-1];
        }
        pila = pilaTemp;
        System.out.println("Pila actual: " + this);
    }

    /**
     * Método principal que permite la interacción del usuario con la pila.
     * <p>
     * Se presenta un menú interactivo que permite al usuario:
     * <ul>
     *   <li>Agregar un elemento a la pila.</li>
     *   <li>Eliminar uno o más elementos del tope de la pila.</li>
     *   <li>Mostrar el contenido actual de la pila.</li>
     *   <li>Salir del programa.</li>
     * </ul>
     * <p>
     * Este método es útil para demostrar el funcionamiento de la estructura de la pila en
     * un entorno interactivo y para facilitar pruebas de concepto en programas que requieran
     * operaciones de apilamiento.
     *
     * @param args argumentos de línea de comandos (no se utilizan en este programa).
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Pilas pila = new Pilas();
        int opcion = 0;

        System.out.println("Bienvenido al simulador de pilas.");

        // Bucle interactivo para el menú de operaciones.
        do {
            System.out.println("\nSeleccione una opción:");
            System.out.println("1. Agregar elemento a la pila");
            System.out.println("2. Eliminar elemento(s) de la pila");
            System.out.println("3. Mostrar la pila actual");
            System.out.println("4. Salir");
            System.out.print("Opción: ");

            // Validación de la entrada para la opción del menú.
            if (scanner.hasNextInt()) {
                opcion = scanner.nextInt();
            } else {
                System.out.println("Entrada inválida. Por favor, ingrese un número entero.");
                scanner.next(); // Limpiar la entrada incorrecta.
                continue;
            }

            // Procesar la opción seleccionada.
            switch (opcion) {
                case 1:
                    System.out.print("Ingrese el elemento a agregar: ");
                    if (scanner.hasNextInt()) {
                        int elemento = scanner.nextInt();
                        pila.agregarElemento(elemento);
                    } else {
                        System.out.println("Entrada inválida. Se esperaba un número entero.");
                        scanner.next();
                    }
                    break;
                case 2:
                    System.out.print("Ingrese la cantidad de elementos a eliminar: ");
                    if (scanner.hasNextInt()) {
                        int cantidad = scanner.nextInt();
                        pila.eliminarElemento(cantidad);
                    } else {
                        System.out.println("Entrada inválida. Se esperaba un número entero.");
                        scanner.next();
                    }
                    break;
                case 3:
                    System.out.println("Pila actual: " + pila);
                    break;
                case 4:
                    System.out.println("Saliendo del programa.");
                    break;
                default:
                    System.out.println("Opción no válida. Intente nuevamente.");
                    break;
            }
        } while (opcion != 4);

        scanner.close();
    }
}