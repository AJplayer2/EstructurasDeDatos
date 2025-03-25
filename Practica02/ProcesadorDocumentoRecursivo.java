package Practica02;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Scanner;
import java.util.List;

/**
 * La clase {@code ProcesadorDocumentoRecursivo} permite la manipulación de un archivo de texto,
 * ofreciendo dos funcionalidades principales: ordenar el contenido de forma lexicográfica y realizar
 * búsquedas recursivas de una cadena, resaltando sus ocurrencias en el texto.
 * <p>
 * Al iniciar el programa, se le da la bienvenida al usuario y se le solicita una ruta o nombre
 * de archivo. Si el archivo no existe o no es de extensión ".txt", se seguirá solicitando una opción válida.
 * Una vez cargado el archivo, se mostrará su contenido original. Luego, el usuario podrá elegir entre:
 * <ol> 
 *   <li>Ordenar el contenido del documento de forma lexicográfica utilizando un algoritmo de ordenamiento
 *       recursivo (Merge Sort).</li>
 *   <li>Buscar una cadena en el documento utilizando algoritmos recursivos para encontrar y resaltar cada ocurrencia.</li>
 * </ol>
 * <p>
 * Este programa utiliza paquetes correspondientes al manejo de archivos y la entrada de datos por teclado.
 *
 * @author Angel Jayden Maya Morales
 */
public class ProcesadorDocumentoRecursivo {

    /**
     * Método principal que inicia la aplicación y gestiona la interacción con el usuario.
     *
     * @param args argumentos de línea de comandos (no se utilizan en este programa).
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String rutaArchivo = "";
        File archivo;
        List<String> lineas = null;

        System.out.println("Bienvenido al procesador de documentos recursivo.");

        // Solicitar al usuario la ruta o nombre del archivo hasta que se ingrese uno válido.
        while (true) {
            System.out.print("Ingrese la ruta o nombre del documento (.txt): ");
            rutaArchivo = scanner.nextLine().trim();
            archivo = new File(rutaArchivo);
            if (!archivo.exists()) {
                System.out.println("El archivo no existe. Intente nuevamente.");
                continue;
            }
            if (!rutaArchivo.toLowerCase().endsWith(".txt")) {
                System.out.println("El archivo no es de formato .txt. Intente nuevamente.");
                continue;
            }
            try {
                // Leer todas las líneas del archivo utilizando el paquete de manejo de archivos.
                lineas = Files.readAllLines(Paths.get(rutaArchivo), StandardCharsets.UTF_8);
            } catch (IOException e) {
                System.out.println("Error al leer el archivo. Intente nuevamente.");
                continue;
            }
            break;
        }

        // Mostrar el contenido original del documento.
        System.out.println("\nContenido del documento:");
        for (String linea : lineas) {
            System.out.println(linea);
        }

        // Menú de opciones para el usuario.
        int opcion = 0;
        do {
            System.out.println("\nSeleccione una opción:");
            System.out.println("1. Ordenar el texto de forma lexicográfica");
            System.out.println("2. Buscar una cadena en el texto");
            System.out.println("3. Salir");
            System.out.print("Opción: ");

            if (scanner.hasNextInt()) {
                opcion = scanner.nextInt();
                scanner.nextLine(); // Limpiar buffer
            } else {
                System.out.println("Entrada inválida. Ingrese un número entero.");
                scanner.next();
                continue;
            }

            switch (opcion) {
                case 1:
                    // Ordenar las líneas utilizando merge sort recursivo.
                    String[] arregloLineas = lineas.toArray(new String[0]);
                    String[] ordenado = mergeSort(arregloLineas);
                    System.out.println("\nTexto ordenado lexicográficamente:");
                    for (String s : ordenado) {
                        System.out.println(s);
                    }
                    break;
                case 2:
                    // Realizar búsqueda recursiva y resaltar las ocurrencias.
                    System.out.print("Ingrese la cadena a buscar: ");
                    String busqueda = scanner.nextLine().trim();
                    System.out.println("\nTexto con las ocurrencias resaltadas (marcadas con >> <<):");
                    int totalOcurrencias = recursiveSearch(lineas.toArray(new String[0]), busqueda, 0);
                    System.out.println("La palabra/frase \"" + busqueda + "\" aparece " + totalOcurrencias + " veces.");
                    break;
                case 3:
                    System.out.println("Saliendo del programa.");
                    break;
                default:
                    System.out.println("Opción no válida. Intente nuevamente.");
                    break;
            }
        } while (opcion != 3);

        scanner.close();
    }

    /**
     * Ordena recursivamente un arreglo de cadenas utilizando el algoritmo Merge Sort.
     * <p>
     * Divide el arreglo en dos mitades, las ordena de forma recursiva y luego las fusiona.
     * Este método es útil para organizar el contenido del documento en orden lexicográfico.
     *
     * @param arr arreglo de cadenas a ordenar.
     * @return un nuevo arreglo de cadenas ordenado lexicográficamente.
     */
    public static String[] mergeSort(String[] arr) {
        if (arr.length <= 1) {
            return arr;
        }
        int mid = arr.length / 2;
        String[] left = new String[mid];
        String[] right = new String[arr.length - mid];

        // Dividir el arreglo en dos mitades.
        for (int i = 0; i < mid; i++) {
            left[i] = arr[i];
        }
        for (int i = mid; i < arr.length; i++) {
            right[i - mid] = arr[i];
        }

        // Ordenar cada mitad de forma recursiva.
        left = mergeSort(left);
        right = mergeSort(right);

        // Fusionar ambas mitades ordenadas.
        return merge(left, right);
    }

    /**
     * Fusiona dos arreglos de cadenas ya ordenados en un solo arreglo ordenado.
     * <p>
     * Este método es utilizado por {@code mergeSort} para combinar las mitades ordenadas.
     *
     * @param left  arreglo de cadenas ordenado.
     * @param right arreglo de cadenas ordenado.
     * @return un nuevo arreglo que contiene los elementos de ambos arreglos en orden lexicográfico.
     */
    private static String[] merge(String[] left, String[] right) {
        String[] result = new String[left.length + right.length];
        int i = 0, j = 0, k = 0;
        // Fusionar los elementos comparando de forma recursiva.
        while (i < left.length && j < right.length) {
            if (left[i].compareToIgnoreCase(right[j]) <= 0) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }
        // Agregar los elementos restantes.
        while (i < left.length) {
            result[k++] = left[i++];
        }
        while (j < right.length) {
            result[k++] = right[j++];
        }
        return result;
    }

    /**
     * Busca recursivamente una cadena en un arreglo de líneas, resalta las ocurrencias y las imprime.
     * <p>
     * Cada línea en la que se encuentre la cadena se imprime con la ocurrencia resaltada mediante
     * el uso de ">>" y "<<" alrededor del texto encontrado.
     *
     * @param lines   arreglo de líneas del documento.
     * @param pattern cadena a buscar.
     * @param index   índice actual en el arreglo para la búsqueda recursiva.
     * @return el número total de ocurrencias encontradas en el arreglo.
     */
    public static int recursiveSearch(String[] lines, String pattern, int index) {
        if (index >= lines.length) {
            return 0;
        }
        // Contar las ocurrencias en la línea actual.
        int count = countOccurrences(lines[index], pattern);
        // Si se encontró al menos una ocurrencia, resaltar y mostrar la línea.
        if (count > 0) {
            System.out.println(highlightOccurrences(lines[index], pattern));
        } else {
            System.out.println(lines[index]);
        }
        // Llamada recursiva para procesar la siguiente línea.
        return count + recursiveSearch(lines, pattern, index + 1);
    }

    /**
     * Resalta recursivamente todas las ocurrencias de una cadena en una línea de texto.
     * <p>
     * Cada ocurrencia se enmarca entre ">>" y "<<" para facilitar su identificación.
     *
     * @param line    línea de texto en la que se realizará la búsqueda.
     * @param pattern cadena que se desea resaltar.
     * @return la línea de texto con las ocurrencias resaltadas.
     */
    public static String highlightOccurrences(String line, String pattern) {
        int index = indexOfIgnoreCase(line, pattern, 0);
        if (index == -1) {
            return line;
        }
        // Separamos la línea en tres partes: antes, la coincidencia y después.
        String before = line.substring(0, index);
        String match = line.substring(index, index + pattern.length());
        String after = line.substring(index + pattern.length());
        // Se resalta la ocurrencia encontrada y se continúa de forma recursiva.
        return before + ">>" + match + "<<" + highlightOccurrences(after, pattern);
    }

    /**
     * Cuenta recursivamente el número de ocurrencias de una cadena en una línea de texto.
     * <p>
     * La comparación se realiza de forma insensible a mayúsculas y minúsculas.
     *
     * @param line    línea de texto en la que se busca la cadena.
     * @param pattern cadena cuya aparición se desea contar.
     * @return el número de veces que la cadena aparece en la línea.
     */
    public static int countOccurrences(String line, String pattern) {
        int index = indexOfIgnoreCase(line, pattern, 0);
        if (index == -1) {
            return 0;
        }
        // Se continúa contando en la subcadena posterior a la ocurrencia encontrada.
        return 1 + countOccurrences(line.substring(index + pattern.length()), pattern);
    }

    /**
     * Busca recursivamente la posición de la primera ocurrencia de una cadena (pattern)
     * en una línea de texto, ignorando diferencias de mayúsculas y minúsculas.
     *
     * @param line    línea de texto en la que se busca.
     * @param pattern cadena a buscar.
     * @param start   posición inicial en la línea para comenzar la búsqueda.
     * @return el índice de la primera ocurrencia o -1 si no se encuentra.
     */
    private static int indexOfIgnoreCase(String line, String pattern, int start) {
        if (start > line.length() - pattern.length()) {
            return -1;
        }
        // Se utiliza regionMatches para comparar ignorando mayúsculas/minúsculas.
        if (line.regionMatches(true, start, pattern, 0, pattern.length())) {
            return start;
        }
        // Se continúa la búsqueda recursivamente a partir del siguiente índice.
        return indexOfIgnoreCase(line, pattern, start + 1);
    }
}
