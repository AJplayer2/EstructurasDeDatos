/**
 * Clase que representa un Banco, permitiendo el manejo de clientes y transacciones bancarias.
 * @author Angel Jayden Maya Morales
 * @version 1.1
 */

 public class Banco {
    private Cliente[] clientes;
    private Transaccion[] transacciones;
    private int numeroClientes;
    private int numeroTransacciones;

    /**
     * Constructor para inicializar un banco con capacidad para 100 clientes y 1000 transacciones.
     */
    public Banco() {
        this.clientes = new Cliente[100];  // Máximo 100 clientes
        this.transacciones = new Transaccion[1000];  // Máximo 1000 transacciones
        this.numeroClientes = 0;
        this.numeroTransacciones = 0;
    }

    /**
     * Agrega un nuevo cliente al banco.
     * @param cliente Cliente a agregar.
     * @throws Exception Si se alcanza el límite de clientes (100).
     */
    public void agregarCliente(Cliente cliente) throws Exception {
        if (numeroClientes == 100) {
            throw new Exception("Número máximo de clientes alcanzado.");
        }
        clientes[numeroClientes] = cliente;
        numeroClientes++;
    }

    /**
     * Elimina un cliente del banco según su ID.
     * @param id Identificación del cliente.
     * @throws Exception Si el cliente no existe o no hay clientes en el banco.
     */
    public void eliminarCliente(String id) throws Exception {
        if (numeroClientes == 0) {
            throw new Exception("No hay clientes registrados.");
        }
        boolean encontrado = false;
        int indiceEncontrado = -1;

        for (int i = 0; i < numeroClientes; i++) {
            if (clientes[i].getId().equals(id)) {
                encontrado = true;
                indiceEncontrado = i;
                break;
            }
        }

        if (!encontrado) {
            throw new Exception("No se encontró un cliente con el ID especificado.");
        }

        // Desplazar elementos hacia la izquierda
        for (int i = indiceEncontrado; i < numeroClientes - 1; i++) {
            clientes[i] = clientes[i + 1];
        }

        clientes[numeroClientes - 1] = null;
        numeroClientes--;
    }

    /**
     * Busca un cliente en el banco según su ID.
     * @param id Identificación del cliente.
     * @return Cliente encontrado.
     * @throws Exception Si el cliente no existe.
     */
    public Cliente buscarCliente(String id) throws Exception {
        for (int i = 0; i < numeroClientes; i++) {
            if (clientes[i].getId().equals(id)) {
                return clientes[i];
            }
        }
        throw new Exception("El ID no coincide con ningún cliente.");
    }

    /**
     * Muestra la lista de clientes registrados en el banco.
     */
    public void mostrarClientes() {
        if (numeroClientes == 0) {
            System.out.println("No hay clientes registrados.");
            return;
        }
        System.out.println("Clientes registrados:");
        for (int i = 0; i < numeroClientes; i++) {
            System.out.println(clientes[i].toString());
        }
    }

    /**
     * Registra una nueva transacción en el banco.
     * @param transaccion Transacción a registrar.
     * @throws Exception Si se alcanzó el límite de transacciones (1000).
     */
    public void registrarTransaccion(Transaccion transaccion) throws Exception {
        if (numeroTransacciones == 1000) {
            throw new Exception("Número máximo de transacciones alcanzado.");
        }
        transacciones[numeroTransacciones] = transaccion;
        numeroTransacciones++;
    }

    /**
     * Muestra todas las transacciones registradas en el banco.
     */
    public void mostrarTransacciones() {
        if (numeroTransacciones == 0) {
            System.out.println("No hay transacciones registradas.");
            return;
        }
        System.out.println("Historial de transacciones:");
        for (int i = 0; i < numeroTransacciones; i++) {
            transacciones[i].mostrarHistorial();
        }
    }

    /**
     * Busca todas las transacciones realizadas con una cuenta bancaria específica.
     * @param numeroCuenta Número de cuenta a buscar.
     */
    public void buscarTransaccionesPorCuenta(int numeroCuenta) {
        boolean encontrado = false;
        System.out.println("Transacciones de la cuenta " + numeroCuenta + ":");
        for (int i = 0; i < numeroTransacciones; i++) {
            if (transacciones[i].getCuentaOrigen().getNumeroCuenta() == numeroCuenta || 
                transacciones[i].getCuentaDestino().getNumeroCuenta() == numeroCuenta) {
                transacciones[i].mostrarHistorial();
                encontrado = true;
            }
        }
        if (!encontrado) {
            System.out.println("No se encontraron transacciones para la cuenta " + numeroCuenta + ".");
        }
    }
}
