# distutils: language = c
# cython: language_level=3
# -*- coding: utf-8 -*-
"""
Implementación manual y optimizada de una Cola (Queue) usando Cython
con un buffer circular basado en un array C de punteros a objetos Python.
"""

# Importar funciones C para manejo de memoria y objetos Python
from libc.stdlib cimport malloc, free
from cpython.ref cimport PyObject, Py_INCREF, Py_DECREF

# Definición de la clase Cython
cdef class CythonQueue:
    # --- Atributos C definidos con cdef ---
    cdef PyObject** items          # Puntero a un array C de punteros a objetos Python (PyObject*)
    cdef int head                # Índice del próximo elemento a sacar (dequeue)
    cdef int tail                # Índice donde se insertará el próximo elemento (enqueue)
    cdef int count               # Número actual de elementos en la cola
    cdef int capacity            # Tamaño actual del array 'items'
    cdef int initial_capacity    # Capacidad inicial con la que empieza la cola

    def __init__(self, int initial_capacity=10):
        """
        Inicializa la cola Cython.

        Args:
            initial_capacity: Tamaño inicial del buffer interno (defecto: 10).
                              Debe ser mayor que 0.
        """
        if initial_capacity <= 0:
            raise ValueError("La capacidad inicial debe ser mayor que 0")

        self.initial_capacity = initial_capacity
        self.capacity = initial_capacity
        # Asignar memoria C para el array de punteros a objetos Python
        # sizeof(PyObject*) es el tamaño de un puntero
        self.items = <PyObject**>malloc(self.capacity * sizeof(PyObject*))
        # Verificar si la asignación de memoria falló
        if not self.items:
            raise MemoryError("No se pudo asignar memoria para la cola")

        # Inicializar índices y contador
        self.head = 0
        self.tail = 0
        self.count = 0
        # Inicializar todos los punteros a NULL (importante)
        for i in range(self.capacity):
            self.items[i] = NULL

    def __dealloc__(self):
        """
        Método especial de Cython llamado cuando el objeto es destruido.
        Libera la memoria C y decrementa contadores de referencia.
        """
        # Decrementar la referencia de todos los objetos Python restantes en el buffer
        if self.items: # Verificar si items fue asignado
            for i in range(self.capacity):
                if self.items[i] != NULL:
                    Py_DECREF(<object>self.items[i]) # Decrementar contador de referencia
            # Liberar la memoria del array C
            free(self.items)
            self.items = NULL # Evitar doble liberación

    cpdef int size(self):
        """Devuelve el número actual de elementos en la cola."""
        return self.count

    cpdef bint isEmpty(self):
        """Comprueba si la cola está vacía."""
        return self.count == 0

    cdef _resize(self, int new_capacity):
        """Redimensiona el buffer interno a una nueva capacidad."""
        print(f"CythonQueue: Redimensionando de {self.capacity} a {new_capacity}") # Debug
        # Asignar nuevo bloque de memoria C
        new_items = <PyObject**>malloc(new_capacity * sizeof(PyObject*))
        if not new_items:
            raise MemoryError("No se pudo asignar memoria para redimensionar la cola")

        # Copiar elementos existentes al nuevo array, manteniendo el orden FIFO
        # y manejando el posible 'wrap-around' del buffer circular
        cdef int i, j
        j = 0
        for i in range(self.count):
            idx = (self.head + i) % self.capacity # Índice en el array viejo
            new_items[j] = self.items[idx] # Copiar puntero (no necesita INCREF aquí)
            self.items[idx] = NULL # Limpiar puntero viejo (evita doble DECREF)
            j += 1

        # Inicializar el resto del nuevo array a NULL
        for i in range(j, new_capacity):
            new_items[i] = NULL

        # Liberar la memoria del array viejo
        free(self.items)

        # Actualizar atributos con el nuevo array y capacidad
        self.items = new_items
        self.head = 0 # El nuevo head siempre empieza en 0
        self.tail = self.count # El nuevo tail es el número de elementos copiados
        self.capacity = new_capacity

    cpdef enqueue(self, object item):
        """Añade un elemento al final de la cola."""
        # Verificar si el buffer está lleno y redimensionar si es necesario
        if self.count == self.capacity:
            # Estrategia de crecimiento (ej. duplicar capacidad)
            new_capacity = self.capacity * 2 if self.capacity > 0 else self.initial_capacity
            self._resize(new_capacity)

        # Incrementar el contador de referencia del objeto Python a añadir
        Py_INCREF(item)
        # Guardar el puntero al objeto en la posición 'tail'
        self.items[self.tail] = <PyObject*>item
        # Mover 'tail' a la siguiente posición, con 'wrap-around'
        self.tail = (self.tail + 1) % self.capacity
        # Incrementar el número de elementos
        self.count += 1

    cpdef object dequeue(self):
        """
        Elimina y devuelve el elemento al frente de la cola.
        Lanza IndexError si la cola está vacía.
        """
        if self.isEmpty():
            raise IndexError("dequeue desde una cola vacía")

        # Obtener el puntero al objeto en la posición 'head'
        cdef PyObject* item_ptr = self.items[self.head]

        # --- IMPORTANTE: Manejo de Referencias ---
        # 1. Convertir el puntero C a objeto Python (esto INCREMENTA su ref count)
        py_item = <object>item_ptr
        # 2. Limpiar la posición en nuestro array C
        self.items[self.head] = NULL
        # 3. Mover 'head' a la siguiente posición, con 'wrap-around'
        self.head = (self.head + 1) % self.capacity
        # 4. Decrementar el número de elementos
        self.count -= 1
        # 5. Decrementar la referencia original que teníamos en el array C
        Py_DECREF(py_item)
        # 6. Devolver el objeto Python (que ahora tiene el ref count correcto)
        return py_item


    cpdef object peek(self):
        """
        Devuelve el elemento al frente de la cola sin eliminarlo.
        Lanza IndexError si la cola está vacía.
        """
        if self.isEmpty():
            raise IndexError("peek en una cola vacía")
        # Devolver el objeto Python directamente (Cython maneja ref count aquí)
        return <object>self.items[self.head]

    # Método para obtener la lista (necesario para TaskModel)
    # Devuelve una *nueva* lista Python con los elementos actuales
    cpdef list get_items_list(self):
        """
        Devuelve una nueva lista Python con los elementos de la cola
        en orden FIFO.
        """
        cdef list result_list = []
        cdef int i
        for i in range(self.count):
            idx = (self.head + i) % self.capacity
            # Convertir puntero a objeto y añadir a la lista (maneja ref count)
            result_list.append(<object>self.items[idx])
        return result_list

    # Métodos mágicos para una mejor integración con Python
    def __len__(self):
        return self.count

    def __iter__(self):
        """Permite iterar sobre los elementos de la cola en orden FIFO."""
        cdef int i
        for i in range(self.count):
            idx = (self.head + i) % self.capacity
            yield <object>self.items[idx] # yield maneja ref counting

    def __repr__(self):
        """Representación textual de la cola."""
        items_str = ", ".join(repr(item) for item in self)
        return f"CythonQueue([{items_str}])"