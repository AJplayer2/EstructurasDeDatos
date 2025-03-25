public class CuentaBancaria {
    // Número único de la cuenta bancaria
    private int numeroCuenta;
    
    // Saldo disponible en la cuenta
    private double saldo;
    
    // Tipo de cuenta: "Ahorros" o "Cheques"
    private String tipo;  

    /**
     * Constructor de la clase CuentaBancaria.
     * Inicializa una cuenta bancaria con un número y tipo de cuenta.
     * El saldo inicial es 0.
     * 
     * @param numeroCuenta Número de la cuenta bancaria.
     * @param tipo Tipo de cuenta ("Ahorros" o "Cheques").
     */
    public CuentaBancaria(int numeroCuenta, String tipo) {
        this.numeroCuenta = numeroCuenta;
        this.tipo = tipo;
        this.saldo = 0.0;
    }

    /**
     * Obtiene el número de cuenta.
     * 
     * @return Número de cuenta bancaria.
     */
    public int getNumeroCuenta() { return numeroCuenta; }

    /**
     * Obtiene el saldo actual de la cuenta.
     * 
     * @return Saldo disponible en la cuenta.
     */
    public double getSaldo() { return saldo; }

    /**
     * Obtiene el tipo de cuenta.
     * 
     * @return Tipo de cuenta ("Ahorros" o "Cheques").
     */
    public String getTipo() { return tipo; }

    /**
     * Realiza un depósito en la cuenta bancaria.
     * 
     * @param monto Cantidad de dinero a depositar.
     * @throws Exception Si el monto es menor o igual a 0.
     */
    public void depositar(double monto) throws Exception {
        if (monto <= 0) {
            throw new Exception("El monto a depositar debe ser mayor a 0");
        }
        this.saldo += monto;
    }

    /**
     * Realiza un retiro de la cuenta bancaria.
     * 
     * @param monto Cantidad de dinero a retirar.
     * @throws Exception Si el monto es menor o igual a 0 o si el saldo es insuficiente.
     */
    public void retirar(double monto) throws Exception {
        if (monto <= 0) {
            throw new Exception("El monto a retirar debe ser mayor a 0");
        }
        if (monto > saldo) {
            throw new Exception("Saldo insuficiente para el retiro");
        }
        saldo -= monto;
    }
}
