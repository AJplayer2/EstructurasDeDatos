import java.util.Scanner;

/**
 * La clase {@code NReinas} implementa la solución al problema de las n-reinas mediante
 * el algoritmo de backtracking. El problema consiste en colocar n reinas en un tablero n×n
 * de forma que ninguna se ataque mutuamente, es decir, no haya más de una reina en la misma
 * fila, columna o diagonal.
 * <p>
 * El programa saluda al usuario, le solicita su nombre y el tamaño del tablero (entre 4 y 7),
 * y luego muestra todas las soluciones enumeradas, representando cada solución en forma de
 * tablero, donde "Q" indica una reina y "." una casilla vacía.
 * </p>
 * 
 * @author Angel Jayden Maya Morales
 */
public class NReinas {

    private int n;                // Tamaño del tablero (n×n)
    private int[] solution;       // Array donde el índice es la fila y el valor la columna donde se coloca la reina
    private int solutionCount;    // Contador de soluciones encontradas

    /**
     * Constructor de la clase.
     *
     * @param n el tamaño del tablero
     */
    public NReinas(int n) {
        this.n = n;
        this.solution = new int[n];
        this.solutionCount = 0;
    }

    /**
     * Inicia el proceso de búsqueda de soluciones mediante backtracking.
     */
    public void solve() {
        placeQueen(0);
    }

    /**
     * Método recursivo que intenta colocar una reina en cada fila del tablero.
     *
     * @param row la fila actual donde se intenta colocar una reina.
     */
    private void placeQueen(int row) {
        if (row == n) {
            // Se ha colocado una reina en cada fila, se encontró una solución.
            solutionCount++;
            System.out.println("Solución " + solutionCount + ":");
            printSolution();
        } else {
            // Se prueba cada columna para la fila actual.
            for (int col = 0; col < n; col++) {
                if (isSafe(row, col)) {
                    solution[row] = col;
                    placeQueen(row + 1);
                }
            }
        }
    }

    /**
     * Verifica si es seguro colocar una reina en la posición (row, col).
     * <p>
     * Se comprueba que no exista otra reina en la misma columna ni en las diagonales.
     * </p>
     *
     * @param row la fila donde se desea colocar la reina.
     * @param col la columna donde se desea colocar la reina.
     * @return {@code true} si es seguro colocar la reina, {@code false} de lo contrario.
     */
    private boolean isSafe(int row, int col) {
        for (int i = 0; i < row; i++) {
            // Misma columna o diagonal
            if (solution[i] == col || Math.abs(solution[i] - col) == row - i) {
                return false;
            }
        }
        return true;
    }

    /**
     * Imprime la solución actual en forma de tablero.
     */
    private void printSolution() {
        for (int i = 0; i < n; i++) {
            // Por cada fila se imprime un renglón con n casillas
            for (int j = 0; j < n; j++) {
                if (solution[i] == j) {
                    System.out.print("Q ");
                } else {
                    System.out.print(". ");
                }
            }
            System.out.println();
        }
        System.out.println();
    }

    /**
     * Método principal que permite la interacción con el usuario.
     * <p>
     * Se solicita el nombre del usuario y el tamaño del tablero (entre 4 y 7), y luego se muestran
     * todas las soluciones posibles al problema de las n-reinas enumeradas.
     * </p>
     *
     * @param args argumentos de línea de comandos (no se utilizan).
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Bienvenido al problema de las n-reinas.");
        System.out.print("Ingrese su nombre: ");
        String nombre = scanner.nextLine();

        int tamano;
        while (true) {
            System.out.print("Ingrese el tamaño del tablero (entre 4 y 7): ");
            tamano = scanner.nextInt();
            if (tamano >= 4 && tamano <= 7) {
                break;
            } else {
                System.out.println("El tamaño debe estar entre 4 y 7. Inténtalo de nuevo.");
            }
        }

        System.out.println("\nHola " + nombre + ", todas las soluciones de tu tablero de " + tamano + "x" + tamano + " son las siguientes:\n");

        NReinas nReinas = new NReinas(tamano);
        nReinas.solve();

        if (nReinas.solutionCount == 0) {
            System.out.println("No se encontraron soluciones.");
        } else {
            System.out.println("Número total de soluciones: " + nReinas.solutionCount);
        }
        scanner.close();
    }
}
