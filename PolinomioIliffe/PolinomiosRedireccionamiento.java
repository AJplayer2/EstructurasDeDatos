public class PolinomiosRedireccionamiento{
    //Metodo para hacer la nueva matriz unidimencional en base al criterio de renglon mayor
    public static int[] RenglonMayor(int[][] matriz){
        //creamos la nueva matriz con tamaño 9
        int[] nuevaMatriz = new int[9];
        //creamos el indice para llenar la nueva matriz
        int indice = 0;
        //llenamos la nueva matriz
        for(int[] i : matriz){
            for(int numCopiar = 0; numCopiar<i.length;numCopiar++){
                nuevaMatriz[indice]=i[numCopiar];
                indice++;
            }
        }
        //regresamos la nueva matriz
        return nuevaMatriz;
    }
    //Metodo para hacer la nueva matriz unidimencional en base al criterio de columna mayor
    public static int[] ColumnaMayor(int[][] matriz){
        //creamos la nueva matriz de tamaño 9
        int[] nuevaMatriz = new int[9];
        //creamos el indice que nos ayudara a llenar la nueva matriz
        int indice = 0;
        //llenamos la nueva matriz
        for(int i = 0; i<3; i++){
            for(int j=0;j<3;j++){
                nuevaMatriz[indice]=matriz[j][i];
                indice++;
            }
        }
        //regresamos la nueva matriz
        return nuevaMatriz;
    }
    //Metodo para encontrar el nuevo indice en un arreglo creado mediante el criterio de Renglon mayor
    public static int indiceRenglonMayor(int ren, int col){
        return (ren*3)+col;
    }
    //Metodo para encontrar el nuevo indice en un arreglo creado mediante el criterio de Columna mayor
    public static int indiceColumnaMayor(int ren, int col){
        return (col*3)+ren;
    }
    //Metodo para mostrar la matriz original
    public static void mostrarMatriz(int[][] matriz){
        for(int i = 0; i<3 ; i++){
            for(int j = 0; j<3; j++){
                System.out.print(matriz[i][j]);
                System.out.print(" ");
            }
            System.out.print('\n');
        }
    }
    //Metodo para crear la mtariz 3 x 3 sobre la que se trabajara
    public static int[][] crearMatriz(){
        int[][] matriz = new int[3][3];
        int indice = 1;
        for(int i = 0; i<3 ; i++){
            for(int j = 0; j<3; j++){
                matriz[i][j]=indice;
                indice++;
            }
        }
        return matriz;
    }
    //Metodo principal
    public static void main(String[] args){
        //creamos la matriz original
        int[][] matriz = crearMatriz();
        //imprimimos la matriz original
        System.out.println("La matriz original es:\n");
        mostrarMatriz(matriz);
        //creamos las dos nuevas matrices, una para cada metodo de creacion
        int[] nuevaMatrizRenglon = RenglonMayor(matriz);
        int[] nuevaMatrizColumna = ColumnaMayor(matriz);
        //imprimimos las nuevas matrices
       System.out.println("Las nuevas matrices son:\nCon el metodo de Columna Mayor:\n"); 
        for(int i : nuevaMatrizColumna){
            System.out.print(i);
            System.out.print(" ");
        }
        System.out.println("\nCon el metodo de Renglon Mayor:\n");
        for(int i : nuevaMatrizRenglon){
            System.out.print(i);
            System.out.print(" ");
        }
        //imprimimos un ejemplo de cada uno de los nuevos indices
        System.out.println("\nEl nuevo indice de la matriz creadad mediante el criterio de columna mayor del numero en la columna 2 y la renglon 3 es:");
        System.out.println(indiceColumnaMayor(2, 1));
        System.out.println("El nuevo indice del mismo numero pero en la matriz creada mediante el criterio de Renglon Mayor es:");
        System.out.println(indiceRenglonMayor(2, 1));
    }
}