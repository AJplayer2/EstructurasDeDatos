import java.util.Random;

public class EjercicioExtraLaberinto {
    private static Random random = new Random();
    private static int r = random.nextInt(3,5);
    private static int[][] matriz = new int[r][r];

    public static void llenarMatriz(){
        for(int[] renglon : matriz){
            for(int i = 0; i<renglon.length; i++){
                renglon[i] = random.nextInt(51);
            }
        }
    }
    public static int[] caminoMayorSuma(){
        int[] caminoMayor = new int[2*r];
        for(int i = 0; i<r*2; i++){
            
        }
    }
    public static int[] valoresPosibles(int renglon, int columna){
        int[] valoresPosibles = new int[3];
        int detenido = 0;
        if(renglon==r-1||columna==r-1){
            if(renglon==columna)return valoresPosibles;
            if(renglon == r-1)detenido=1;
            if(columna == r-1)detenido=-1;
        }
        switch (detenido) {
            case 0:
                valoresPosibles[0]=matriz[renglon][columna+1];
                valoresPosibles[1]=matriz[renglon+1][columna+1];
                valoresPosibles[2]=matriz[renglon+1][columna];
            case 1:
                valoresPosibles[0]=matriz[r-1][columna+1];
                valoresPosibles[1]=-1;
            case -1:
                valoresPosibles[0]=-1;
                valoresPosibles[2]=matriz[renglon+1][r-1];
        }
        return valoresPosibles;
    }
}

