from collections import deque
from .Task import Task as task

#Clase cola especial para las tareas, se usa deque para mejorar la eficiencia de tiempo en comparacion a listas
class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item:task):
        self.items.append(item)

    #IndexError para simular el comportamiento de una cola
    def dequeue(self):
        if not self.isEmpty():
            return self.items.popleft()
        raise IndexError("Dequeue from empty queue")

    def removeTask(self, item:task):
        self.items.remove(item)

    def isEmpty(self):
        return len(self.items)==0
    
    def size(self):
        return len(self.items)