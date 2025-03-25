import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Banco banco = new Banco();

        System.out.println("¡Bienvenido al sistema bancario!");

        while (true) {
            System.out.println("""
                ----------------------------
                1. Agregar Cliente
                2. Agregar Cuenta Bancaria
                3. Realizar Transacción
                4. Eliminar Cliente
                5. Mostrar Clientes y sus Cuentas
                6. Mostrar Historial de Transacciones
                7. Salir
                ----------------------------
                Elige una opción:
                """);

                int opcion = scanner.nextInt();
            scanner.nextLine();  // Limpiar buffer

            switch (opcion) {
                case 1 -> agregarCliente(banco, scanner);
                case 2 -> agregarCuenta(banco, scanner);
                case 3 -> realizarTransaccion(banco, scanner);
                case 4 -> eliminarCliente(banco, scanner);
                case 5 -> banco.mostrarClientes();
                case 6 -> banco.mostrarTransacciones();
                case 7 -> {
                    System.out.println("Gracias por usar el sistema bancario.");
                    scanner.close();
                    return;
                }
                default -> System.out.println("Opción inválida. Inténtelo de nuevo.");
            }
        }
    }

    private static void agregarCliente(Banco banco, Scanner scanner) {
        System.out.print("Ingrese el nombre del cliente: ");
        String nombre = scanner.nextLine();
        System.out.print("Ingrese el ID del cliente: ");
        String id = scanner.nextLine();

        try {
            banco.agregarCliente(new Cliente(nombre, id));
            System.out.println("Cliente agregado exitosamente.");
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    private static void agregarCuenta(Banco banco, Scanner scanner) {
        System.out.print("Ingrese el ID del cliente: ");
        String id = scanner.nextLine();

        try {
            Cliente cliente = banco.buscarCliente(id);
            System.out.print("Ingrese el número de cuenta: ");
            int numeroCuenta = scanner.nextInt();
            scanner.nextLine();  // Limpiar buffer
            System.out.print("Ingrese el tipo de cuenta (Ahorros o Cheques): ");
            String tipo = scanner.nextLine();

            cliente.agregarCuenta(new CuentaBancaria(numeroCuenta, tipo));
            System.out.println("Cuenta agregada exitosamente.");
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    private static void realizarTransaccion(Banco banco, Scanner scanner) {
        System.out.print("Ingrese el ID del cliente de la cuenta origen: ");
        String idOrigen = scanner.nextLine();

        try {
            Cliente clienteOrigen = banco.buscarCliente(idOrigen);
            System.out.print("Ingrese el número de cuenta origen: ");
            int numCuentaOrigen = scanner.nextInt();
            scanner.nextLine();

            System.out.print("Ingrese el ID del cliente de la cuenta destino: ");
            String idDestino = scanner.nextLine();
            Cliente clienteDestino = banco.buscarCliente(idDestino);
            System.out.print("Ingrese el número de cuenta destino: ");
            int numCuentaDestino = scanner.nextInt();
            scanner.nextLine();

            System.out.print("Ingrese el monto: ");
            double monto = scanner.nextDouble();
            scanner.nextLine();

            System.out.print("Ingrese el tipo de transacción (Deposito o Retiro): ");
            String tipo = scanner.nextLine();

            CuentaBancaria cuentaOrigen = null;
            CuentaBancaria cuentaDestino = null;

            // Buscar la cuenta origen en el cliente
            for (CuentaBancaria c : clienteOrigen.getCuentas()) {
                if (c != null && c.getNumeroCuenta() == numCuentaOrigen) {
                    cuentaOrigen = c;
                    break;
                }
            }

            // Buscar la cuenta destino en el cliente
            for (CuentaBancaria c : clienteDestino.getCuentas()) {
                if (c != null && c.getNumeroCuenta() == numCuentaDestino) {
                    cuentaDestino = c;
                    break;
                }
            }

            if (cuentaOrigen == null || cuentaDestino == null) {
                System.out.println("Error: Una de las cuentas no existe.");
                return;
            }

            Transaccion transaccion = new Transaccion(cuentaOrigen, cuentaDestino, monto, tipo);
            transaccion.registrar();
            banco.registrarTransaccion(transaccion);
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    private static void eliminarCliente(Banco banco, Scanner scanner) {
        System.out.print("Ingrese el ID del cliente a eliminar: ");
        String id = scanner.nextLine();

        try {
            banco.eliminarCliente(id);
            System.out.println("Cliente eliminado exitosamente.");
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
