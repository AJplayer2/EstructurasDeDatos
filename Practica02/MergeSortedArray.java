package Practica02;
import java.util.Scanner;

/**
 * La clase {@code MergeSortedArray} contiene métodos para fusionar dos arreglos
 * de enteros ordenados en uno solo, utilizando un algoritmo de complejidad lineal.
 * <p>
 * Se considera que los arreglos de entrada están ordenados en forma ascendente.
 * Este método es útil en aplicaciones que requieren la combinación eficiente
 * de conjuntos de datos ordenados.
 * </p>
 * 
 * @author Angel Jayden Maya Morales
 */
public class MergeSortedArray {

    /**
     * Fusiona dos arreglos de enteros ordenados en uno solo, manteniendo el orden ascendente.
     * <p>
     * El método recorre ambos arreglos de forma simultánea y copia el elemento menor
     * de cada uno en el arreglo resultado. De esta forma, la fusión se realiza en complejidad
     * lineal, es decir, O(n + m), donde {@code n} y {@code m} son los tamaños de los arreglos de entrada.
     * </p>
     *
     * @param array1 primer arreglo de enteros ordenado.
     * @param n cantidad de elementos a considerar en {@code array1}.
     * @param array2 segundo arreglo de enteros ordenado.
     * @param m cantidad de elementos a considerar en {@code array2}.
     * @return un nuevo arreglo que contiene los elementos de {@code array1} y {@code array2} en orden ascendente.
     * @throws RuntimeException si {@code n} o {@code m} superan la longitud de {@code array1} o {@code array2}, respectivamente.
     */
    public static int[] mergeSortedArray(int[] array1, int n, int[] array2, int m) {
        if (n > array1.length || m > array2.length) {
            throw new RuntimeException("Limites no validos");
        }
        int[] result = new int[n + m];
        int i = 0, j = 0, k = 0;

        // Fusiona ambos arreglos recorriéndolos de forma simultánea.
        while (i < n && j < m) {
            if (array1[i] <= array2[j]) {
                result[k++] = array1[i++];
            } else {
                result[k++] = array2[j++];
            }
        }
        // Agrega los elementos restantes de array1 (si existen).
        while (i < n) {
            result[k++] = array1[i++];
        }
        // Agrega los elementos restantes de array2 (si existen).
        while (j < m) {
            result[k++] = array2[j++];
        }
        return result;
    }

    /**
     * Método principal para probar la fusión de arreglos ordenados.
     * <p>
     * Permite al usuario ingresar dos arreglos de enteros ya ordenados y muestra el arreglo resultante
     * tras fusionarlos en orden ascendente.
     * </p>
     *
     * @param args argumentos de línea de comandos (no se utilizan).
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Ingrese el número de elementos del primer arreglo:");
        int n = scanner.nextInt();
        int[] array1 = new int[n];
        System.out.println("Ingrese " + n + " elementos ordenados para el primer arreglo:");
        for (int i = 0; i < n; i++) {
            array1[i] = scanner.nextInt();
        }

        System.out.println("Ingrese el número de elementos del segundo arreglo:");
        int m = scanner.nextInt();
        int[] array2 = new int[m];
        System.out.println("Ingrese " + m + " elementos ordenados para el segundo arreglo:");
        for (int i = 0; i < m; i++) {
            array2[i] = scanner.nextInt();
        }

        int[] mergedArray = mergeSortedArray(array1, n, array2, m);

        System.out.println("Arreglo fusionado en orden ascendente:");
        for (int num : mergedArray) {
            System.out.print(num + " ");
        }
        System.out.println();
        scanner.close();
    }
}
