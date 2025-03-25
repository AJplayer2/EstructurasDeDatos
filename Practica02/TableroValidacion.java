package Practica02;

import java.util.Scanner;

/**
 * La clase {@code TableroValidacion} determina si un tablero de tamaño n×n contiene
 * exactamente los elementos de 0 a n−1 en cada fila y columna, sin repeticiones.
 * <p>
 * El programa solicita al usuario el tamaño del tablero y sus elementos, y luego verifica
 * si cada fila y cada columna contienen los números en el rango indicado sin duplicados.
 * </p>
 * 
 * @author Angel Jayden Maya Morales
 */
public class TableroValidacion {

    /**
     * Verifica si el tablero cumple que cada fila y cada columna contengan los números
     * de 0 a n−1 sin repetirse.
     * <p>
     * Para cada fila y cada columna se utiliza un arreglo booleano para marcar la aparición
     * de cada número. Si se detecta un número fuera del rango o duplicado, se retorna {@code false}.
     * </p>
     *
     * @param board matriz de enteros que representa el tablero.
     * @return {@code true} si el tablero es válido; {@code false} en caso contrario.
     */
    public static boolean isValidBoard(int[][] board) {
        int n = board.length;
        
        // Verificar cada fila
        for (int i = 0; i < n; i++) {
            boolean[] seen = new boolean[n];
            for (int j = 0; j < n; j++) {
                int num = board[i][j];
                // Validar que el número esté dentro del rango [0, n-1]
                if (num < 0 || num >= n) {
                    return false;
                }
                // Si el número ya fue encontrado en la fila, es duplicado.
                if (seen[num]) {
                    return false;
                }
                seen[num] = true;
            }
        }
        
        // Verificar cada columna
        for (int j = 0; j < n; j++) {
            boolean[] seen = new boolean[n];
            for (int i = 0; i < n; i++) {
                int num = board[i][j];
                // Validar que el número esté dentro del rango [0, n-1]
                if (num < 0 || num >= n) {
                    return false;
                }
                // Si el número ya fue encontrado en la columna, es duplicado.
                if (seen[num]) {
                    return false;
                }
                seen[num] = true;
            }
        }
        return true;
    }

    /**
     * Método principal que permite al usuario interactuar con el programa.
     * <p>
     * Se solicita al usuario el tamaño del tablero (n) y luego los elementos del mismo.
     * Tras la entrada, se verifica si el tablero es válido y se muestra el resultado por consola.
     * </p>
     *
     * @param args argumentos de línea de comandos (no se utilizan).
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese el tamaño del tablero (n): ");
        int n = scanner.nextInt();
        
        int[][] board = new int[n][n];
        System.out.println("Ingrese los elementos del tablero (valores entre 0 y " + (n - 1) + "):");
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                System.out.print("Elemento [" + i + "][" + j + "]: ");
                board[i][j] = scanner.nextInt();
            }
        }
        
        boolean valid = isValidBoard(board);
        if (valid) {
            System.out.println("El tablero es válido.");
        } else {
            System.out.println("El tablero es inválido.");
        }
        scanner.close();
    }
}
