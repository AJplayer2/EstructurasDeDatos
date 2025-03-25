/**
 * Clase que representa a un cliente del banco.
 * Un cliente puede tener hasta 5 cuentas bancarias.
 * @author Angel Jayden Maya Morales
 * @version 1.0
 */
public class Cliente {
    private String nombre;
    private String id;
    private CuentaBancaria[] cuentas;
    private int cuentasOcupadas;

    /**
     * Constructor de Cliente.
     * @param nombre Nombre del cliente.
     * @param id Identificación única del cliente.
     */
    public Cliente(String nombre, String id) {
        this.nombre = nombre;
        this.id = id;
        this.cuentas = new CuentaBancaria[5];  // Máximo 5 cuentas por cliente
        this.cuentasOcupadas = 0;
    }

    /**
     * Obtiene el arreglo de las cuentas del cliente.
     * @return el arreglo cuentas[].
     */
    public CuentaBancaria[] getCuentas() { return cuentas; }

    /**
     * Obtiene el nombre del cliente.
     * @return Nombre del cliente.
     */
    public String getNombre() { return nombre; }

    /**
     * Establece el nombre del cliente.
     * @param nombre Nuevo nombre del cliente.
     */
    public void setNombre(String nombre) { this.nombre = nombre; }

    /**
     * Obtiene el ID del cliente.
     * @return ID del cliente.
     */
    public String getId() { return id; }

    /**
     * Establece el ID del cliente.
     * @param id Nuevo ID del cliente.
     */
    public void setId(String id) { this.id = id; }

    /**
     * Agrega una cuenta bancaria al cliente.
     * @param cuenta Cuenta bancaria a agregar.
     */
    public void agregarCuenta(CuentaBancaria cuenta) {
        if (cuentasOcupadas == 5) {
            System.out.println("Número máximo de cuentas bancarias alcanzado, por favor, elimine una cuenta para continuar.");
            return;
        }
        cuentas[cuentasOcupadas] = cuenta;
        cuentasOcupadas++;
    }

    /**
     * Elimina una cuenta bancaria asociada al cliente.
     * @param numeroCuenta Número de la cuenta a eliminar.
     */
    public void eliminarCuenta(int numeroCuenta) {
        boolean encontrado = false;
        int indiceEncontrado = -1;

        // Buscar la cuenta
        for (int i = 0; i < cuentasOcupadas; i++) {
            if (cuentas[i] != null && cuentas[i].getNumeroCuenta() == numeroCuenta) {
                encontrado = true;
                indiceEncontrado = i;
                break;
            }
        }

        if (encontrado) {
            // Desplazar cuentas para llenar el espacio vacío
            for (int i = indiceEncontrado; i < cuentasOcupadas - 1; i++) {
                cuentas[i] = cuentas[i + 1];
            }
            cuentas[cuentasOcupadas - 1] = null;  // Eliminar la última cuenta
            cuentasOcupadas--;
            System.out.println("Cuenta eliminada correctamente.");
        } else {
            System.out.println("ID de la cuenta no encontrado.");
        }
    }

    /**
     * Muestra todas las cuentas asociadas al cliente.
     */
    public void mostrarCuentas() {
        if (cuentasOcupadas == 0) {
            System.out.println("Este cliente no tiene ninguna cuenta asociada, por favor asocie una cuenta lo antes posible.");
            return;
        }
        System.out.println("Las cuentas asociadas a este cliente son:");
        for (int i = 0; i < cuentasOcupadas; i++) {
            System.out.println("Cuenta " + (i + 1) + ": Número " + cuentas[i].getNumeroCuenta() + ", Saldo: " + cuentas[i].getSaldo());
        }
    }
}
