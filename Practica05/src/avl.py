class Nodo:
    """
    Clase para representar un nodo en el árbol AVL.
    """
    def __init__(self, valor):
        """
        Inicializa un nodo.

        Args:
            valor: El valor que almacenará el nodo.
        """
        self.valor = valor
        self.hijo_izquierdo = None
        self.hijo_derecho = None
        self.altura = 1 # Altura inicial de un nodo nuevo es 1

class AVL:
    """
    Clase para representar la estructura de datos Árbol Binario AVL.
    """
    def get_altura(self, nodo):
        """
        Obtiene la altura de un nodo. Retorna 0 si el nodo es None.
        """
        if not nodo:
            return 0
        return nodo.altura

    def get_balance(self, nodo):
        """
        Calcula el factor de balanceo de un nodo.
        """
        if not nodo:
            return 0
        # Factor de balanceo = Altura(subárbol izquierdo) - Altura(subárbol derecho)
        return self.get_altura(nodo.hijo_izquierdo) - self.get_altura(nodo.hijo_derecho)

    def rotacion_derecha(self, z):
        """
        Realiza una rotación simple a la derecha.
        Se aplica cuando el subárbol izquierdo es más alto (balance > 1)
        y la inserción fue en el subárbol izquierdo del hijo izquierdo.
        """
        y = z.hijo_izquierdo
        T3 = y.hijo_derecho

        # Realizar rotación
        y.hijo_derecho = z
        z.hijo_izquierdo = T3

        # Actualizar alturas
        z.altura = 1 + max(self.get_altura(z.hijo_izquierdo), self.get_altura(z.hijo_derecho))
        y.altura = 1 + max(self.get_altura(y.hijo_izquierdo), self.get_altura(y.hijo_derecho))

        # Retornar la nueva raíz del subárbol rotado
        return y

    def rotacion_izquierda(self, y):
        """
        Realiza una rotación simple a la izquierda.
        Se aplica cuando el subárbol derecho es más alto (balance < -1)
        y la inserción fue en el subárbol derecho del hijo derecho.
        """
        x = y.hijo_derecho
        T2 = x.hijo_izquierdo

        # Realizar rotación
        x.hijo_izquierdo = y
        y.hijo_derecho = T2

        # Actualizar alturas
        y.altura = 1 + max(self.get_altura(y.hijo_izquierdo), self.get_altura(y.hijo_derecho))
        x.altura = 1 + max(self.get_altura(x.hijo_izquierdo), self.get_altura(x.hijo_derecho))

        # Retornar la nueva raíz del subárbol rotado
        return x

    def insertar(self, raiz, valor):
        """
        Inserta un valor en el árbol AVL y mantiene el balance.
        """
        # 1. Realizar la inserción estándar de un Árbol Binario de Búsqueda (ABB)
        if not raiz:
            return Nodo(valor)
        elif valor < raiz.valor:
            raiz.hijo_izquierdo = self.insertar(raiz.hijo_izquierdo, valor)
        else:
            raiz.hijo_derecho = self.insertar(raiz.hijo_derecho, valor)

        # 2. Actualizar la altura del nodo ancestro
        raiz.altura = 1 + max(self.get_altura(raiz.hijo_izquierdo),
                           self.get_altura(raiz.hijo_derecho))

        # 3. Obtener el factor de balanceo de este nodo ancestro
        balance = self.get_balance(raiz)

        # 4. Si el nodo está desbalanceado, aplicar rotaciones
        # Caso Izquierda Izquierda (Rotación Simple Derecha)
        if balance > 1 and valor < raiz.hijo_izquierdo.valor:
            return self.rotacion_derecha(raiz)

        # Caso Derecha Derecha (Rotación Simple Izquierda)
        if balance < -1 and valor > raiz.hijo_derecho.valor:
            return self.rotacion_izquierda(raiz)

        # Caso Izquierda Derecha (Rotación Doble Izquierda-Derecha)
        if balance > 1 and valor > raiz.hijo_izquierdo.valor:
            raiz.hijo_izquierdo = self.rotacion_izquierda(raiz.hijo_izquierdo)
            return self.rotacion_derecha(raiz)

        # Caso Derecha Izquierda (Rotación Doble Derecha-Izquierda)
        if balance < -1 and valor < raiz.hijo_derecho.valor:
            raiz.hijo_derecho = self.rotacion_derecha(raiz.hijo_derecho)
            return self.rotacion_izquierda(raiz)

        # Si no hubo desbalanceo, retornar la raíz sin cambios
        return raiz

    # Método auxiliar para imprimir el árbol (puede ser útil para pruebas)
    def preorden(self, raiz):
        """
        Recorrido preorden para imprimir el árbol (Raíz, Izquierda, Derecha).
        """
        if not raiz:
            return
        print(f"{raiz.valor} (Altura: {raiz.altura}, Balance: {self.get_balance(raiz)})", end=" ")
        self.preorden(raiz.hijo_izquierdo)
        self.preorden(raiz.hijo_derecho)

# Ejemplo básico de uso para probar inserciones y balanceo en consola
if __name__ == "__main__":
    arbol_avl = AVL()
    raiz = None

    valores = [30, 20, 40, 10, 25, 5, 15, 27, 35, 50, 1] 

    print("Insertando valores:", valores)
    for valor in valores:
        raiz = arbol_avl.insertar(raiz, valor)
        print(f"\nInsertado {valor}. Árbol actual (preorden):")
        arbol_avl.preorden(raiz)
        print("\n--------------------")

    print("\nÁrbol AVL final (preorden):")
    arbol_avl.preorden(raiz)
    print()