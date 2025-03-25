import java.util.Scanner;

/**
 * Programa que permite ingresar una matriz bidimensional, imprimirla, convertirla
 * a un arreglo unidimensional y buscar elementos con sus índices.
 * No utiliza ArrayLists para almacenar datos.
 */
public class MatrixVectorSearch {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Solicitar tamaño de la matriz
        System.out.println("Ingrese el número de filas de la matriz (max 50): ");
        int filas = obtenerValorValido(scanner, 1, 50);
        System.out.println("Ingrese el número de columnas de la matriz (max 50): ");
        int columnas = obtenerValorValido(scanner, 1, 50);

        // Crear y llenar la matriz
        int[][] matriz = new int[filas][columnas];
        System.out.println("Ingrese los elementos de la matriz:");
        for (int i = 0; i < filas; i++) {
            for (int j = 0; j < columnas; j++) {
                System.out.printf("Elemento [%d][%d]: ", i, j);
                matriz[i][j] = scanner.nextInt();
            }
        }

        // Imprimir matriz
        System.out.println("\nMatriz ingresada:");
        imprimirMatriz(matriz, filas, columnas);

        // Convertir matriz a arreglo unidimensional
        int[] arregloUnidimensional = convertirMatrizAArreglo(matriz, filas, columnas);
        System.out.println("\nArreglo unidimensional:");
        imprimirArreglo(arregloUnidimensional);

        // Buscar elementos en el arreglo
        System.out.println("\nIngrese el elemento que desea buscar: ");
        int elementoBuscado = scanner.nextInt();
        buscarIndices(matriz, arregloUnidimensional, filas, columnas, elementoBuscado);

        scanner.close();
    }

    // Método para obtener un valor entero dentro de un rango válido
    private static int obtenerValorValido(Scanner scanner, int min, int max) {
        int valor;
        while (true) {
            valor = scanner.nextInt();
            if (valor >= min && valor <= max) {
                return valor;
            } else {
                System.out.printf("Por favor ingrese un valor entre %d y %d: ", min, max);
            }
        }
    }

    // Imprime una matriz bidimensional
    private static void imprimirMatriz(int[][] matriz, int filas, int columnas) {
        for (int i = 0; i < filas; i++) {
            for (int j = 0; j < columnas; j++) {
                System.out.printf("%4d", matriz[i][j]);
            }
            System.out.println();
        }
    }

    // Convierte una matriz bidimensional a un arreglo unidimensional
    private static int[] convertirMatrizAArreglo(int[][] matriz, int filas, int columnas) {
        int[] arreglo = new int[filas * columnas];
        int indice = 0;
        for (int i = 0; i < filas; i++) {
            for (int j = 0; j < columnas; j++) {
                arreglo[indice++] = matriz[i][j];
            }
        }
        return arreglo;
    }

    // Imprime un arreglo unidimensional
    private static void imprimirArreglo(int[] arreglo) {
        for (int valor : arreglo) {
            System.out.printf("%4d", valor);
        }
        System.out.println();
    }

    // Busca los índices del elemento en la matriz y en el arreglo
    private static void buscarIndices(int[][] matriz, int[] arreglo, int filas, int columnas, int elemento) {
        boolean encontrado = false;
        System.out.println("\nResultados de la búsqueda:");

        // Búsqueda en la matriz
        for (int i = 0; i < filas; i++) {
            for (int j = 0; j < columnas; j++) {
                if (matriz[i][j] == elemento) {
                    encontrado = true;
                    int indiceArreglo = i * columnas + j;
                    System.out.printf("Elemento encontrado en matriz[%d][%d] y arreglo[%d]\n", i, j, indiceArreglo);
                }
            }
        }

        if (!encontrado) {
            System.out.println("El elemento no se encuentra en la matriz.");
        }
    }
}
