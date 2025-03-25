import java.time.LocalDate;
import java.time.ZoneId;

/**
 * Clase que representa una transacción bancaria entre cuentas.
 * Puede ser un depósito o un retiro.
 * @author Angel Jayden Maya Morales
 * @version 1.1
 */
public class Transaccion {
    private CuentaBancaria cuentaOrigen;
    private CuentaBancaria cuentaDestino;
    private double monto;
    private String tipo;  // "Deposito" o "Retiro"
    private String fecha;

    /**
     * Constructor de la clase Transaccion.
     * @param cuentaOrigen Cuenta desde la cual se hace la transacción.
     * @param cuentaDestino Cuenta que recibe la transacción.
     * @param monto Monto de dinero involucrado en la transacción.
     * @param tipo Tipo de transacción: "Deposito" o "Retiro".
     */
    public Transaccion(CuentaBancaria cuentaOrigen, CuentaBancaria cuentaDestino, double monto, String tipo) {
        this.cuentaOrigen = cuentaOrigen;
        this.cuentaDestino = cuentaDestino;
        this.monto = monto;
        this.tipo = tipo;
        // Asignar la fecha actual de la transacción
        ZoneId zona = ZoneId.of("America/Montreal");
        LocalDate fechaActual = LocalDate.now(zona);
        this.fecha = fechaActual.toString();
    }

    /**
     * Método que ejecuta la transacción entre cuentas.
     * @throws Exception Si el monto es inválido o la cuenta no tiene fondos suficientes.
     */
    public void registrar() throws Exception {
        try {
            switch (tipo) {
                case "Deposito" -> {
                    cuentaOrigen.retirar(monto);
                    cuentaDestino.depositar(monto);
                    System.out.println("Se ha realizado un depósito de la cuenta: " 
                        + cuentaOrigen.getNumeroCuenta() + " a la cuenta: " 
                        + cuentaDestino.getNumeroCuenta() + " por un monto de " + monto + ".");
                }
                case "Retiro" -> {
                    cuentaOrigen.depositar(monto);
                    cuentaDestino.retirar(monto);
                    System.out.println("Se ha realizado un retiro de la cuenta: " 
                        + cuentaDestino.getNumeroCuenta() + ". El dinero fue depositado en la cuenta del banco con ID: " 
                        + cuentaOrigen.getNumeroCuenta() + ".");
                }
                default -> throw new Exception("Tipo de transacción inválido.");
            }
        } catch (Exception e) {
            throw e;
        }
    }

    /**
     * Método que muestra la información de la transacción.
     */
    public void mostrarHistorial() {
        System.out.println("Cuenta Origen: " + cuentaOrigen.getNumeroCuenta() + 
            "; Cuenta Destino: " + cuentaDestino.getNumeroCuenta() + 
            "; Monto: " + monto + "; Tipo: " + tipo + "; Fecha: " + fecha + ".");
    }

    /**
     * Obtiene la cuenta de origen de la transacción.
     * @return La cuenta de origen.
     */
    public CuentaBancaria getCuentaOrigen() {
        return cuentaOrigen;
    }

    /**
     * Obtiene la cuenta de destino de la transacción.
     * @return La cuenta de destino.
     */
    public CuentaBancaria getCuentaDestino() {
        return cuentaDestino;
    }
}
