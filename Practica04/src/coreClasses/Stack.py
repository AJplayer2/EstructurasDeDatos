# -*- coding: utf-8 -*-
# Importar Task sólo para type hinting
from typing import TypeVar, Generic
try:
    # Asumiendo la ubicación de Task después de refactorizar
    from .Task import Task
except ImportError:
    # Definición dummy para type hinting si la importación falla
    Task = TypeVar('Task')

T = TypeVar('T') # Para hacerlo genérico

class Stack(Generic[T]):
    """
    Implementación manual de una Pila (Stack) usando una lista de Python.
    Sigue el principio LIFO (Last-In, First-Out).
    """
    def __init__(self):
        """Inicializa una pila vacía."""
        self._items: list[T] = []

    def push(self, item: T) -> None: # Renombrar append a push es más estándar
        """Añade un elemento a la cima de la pila."""
        self._items.append(item)

    def pop(self) -> T:
        """
        Elimina y devuelve el elemento en la cima de la pila.
        Lanza IndexError si la pila está vacía.
        """
        if not self.isEmpty():
            # list.pop() sin argumento quita el último elemento (LIFO)
            return self._items.pop()
        else:
            raise IndexError("pop desde una pila vacía")

    def peek(self) -> T:
        """
        Devuelve el elemento en la cima de la pila sin eliminarlo.
        Lanza IndexError si la pila está vacía.
        """
        if not self.isEmpty():
            return self._items[-1]
        else:
            raise IndexError("peek en una pila vacía")

    def isEmpty(self) -> bool:
        """Comprueba si la pila está vacía."""
        return len(self._items) == 0

    def size(self) -> int:
        """Devuelve el número de elementos en la pila."""
        return len(self._items)

    def get_items_list(self) -> list[T]:
         """Devuelve una copia de la lista de items (para taskList)."""
         # Devuelve una copia para evitar modificaciones externas
         return list(self._items)

    def __len__(self) -> int:
        """Permite usar len(stack)."""
        return self.size()

    def __iter__(self):
        """Permite iterar sobre la pila (desde fondo a cima)."""
        return iter(self._items)

    def __repr__(self) -> str:
         """Representación textual de la pila."""
         # Mostrar el tope al final para visualización LIFO
         return f"Stack({self._items})"