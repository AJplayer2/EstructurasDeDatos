from .Task import Task as task

#Clase stack especial para las tareas.
class Stack:
    def __init__(self):
        self.items = []
    
    def append(self, item:task):
        self.items.append(item)
    
    #IndexError es para simular bien el comportamiento de un stack
    def pop(self):
        if not self.isEmpty():
            return self.items.pop()
        raise IndexError("Pop from an empty stack")

    def isEmpty(self):
        return len(self.items)==0
    
    def size(self):
        return len(self.items)