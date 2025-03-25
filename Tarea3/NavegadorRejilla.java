package Tarea3;
import java.util.Scanner;

/**
 * Clase que permite simular el movimiento de un navegador en una rejilla MxM,
 * siguiendo una secuencia de movimientos y evitando obstáculos.
 *
 * @author Angel Jayden Maya Morales
 */
public class NavegadorRejilla {
    private static final int[][] DIRECCIONES = {
        {-1,  0}, // U (arriba)
        { 1,  0}, // D (abajo)
        { 0, -1}, // L (izquierda)
        { 0,  1}, // R (derecha)
        {-1, -1}, // a (diagonal arriba-izquierda)
        {-1,  1}, // b (diagonal arriba-derecha)
        { 1, -1}, // c (diagonal abajo-izquierda)
        { 1,  1}  // d (diagonal abajo-derecha)
    };

    private static final char[] MOVIMIENTOS = {'U', 'D', 'L', 'R', 'a', 'b', 'c', 'd'};

    /**
     * Función recursiva que mueve el navegador según la secuencia dada.
     *
     * @param grid     Rejilla MxM (0 = libre, 1 = obstáculo).
     * @param x        Coordenada X actual del navegador.
     * @param y        Coordenada Y actual del navegador.
     * @param moves    Secuencia de movimientos.
     * @param index    Índice actual en la secuencia de movimientos.
     */
    public static void moverNavegador(int[][] grid, int x, int y, String moves, int index) {
        if (index >= moves.length()) {
            System.out.println("Movimiento finalizado en (" + x + ", " + y + ")");
            return;
        }

        char move = moves.charAt(index);
        int dx = 0, dy = 0;
        
        for (int i = 0; i < MOVIMIENTOS.length; i++) {
            if (MOVIMIENTOS[i] == move) {
                dx = DIRECCIONES[i][0];
                dy = DIRECCIONES[i][1];
                break;
            }
        }

        int newX = x + dx;
        int newY = y + dy;

        if (newX < 0 || newX >= grid.length || newY < 0 || newY >= grid[0].length || grid[newX][newY] == 1) {
            System.out.println("Movimiento bloqueado en (" + x + ", " + y + ")");
            return;
        }

        moverNavegador(grid, newX, newY, moves, index + 1);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese el tamaño de la rejilla (M): ");
        int M = scanner.nextInt();

        int[][] grid = new int[M][M];
        System.out.println("Ingrese la rejilla (0 = libre, 1 = obstáculo):");
        for (int i = 0; i < M; i++) {
            for (int j = 0; j < M; j++) {
                grid[i][j] = scanner.nextInt();
            }
        }

        System.out.print("Ingrese la posición inicial (x, y): ");
        int x = scanner.nextInt();
        int y = scanner.nextInt();

        System.out.print("Ingrese la secuencia de movimientos: ");
        String moves = scanner.next();

        moverNavegador(grid, x, y, moves, 0);
        scanner.close();
    }
}
