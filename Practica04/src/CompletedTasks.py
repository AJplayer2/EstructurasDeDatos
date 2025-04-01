# -*- coding: utf-8 -*-
"""
Módulo para gestionar la colección de tareas completadas usando una pila.
"""
# Importar Task refactorizada y Stack refactorizada
from src.coreClasses.Task import Task
from src.coreClasses.Stack import Stack # Usar la Stack manual refactorizada

class CompletedTasks:
    """
    Gestiona la colección de tareas completadas utilizando una implementación
    de Pila (Stack) manual.
    """
    def __init__(self):
        """Inicializa el contenedor de tareas completadas con una pila vacía."""
        self.tasks: Stack[Task] = Stack() # Usar la Stack manual refactorizada

    def addTask(self, item: Task) -> None:
        """
        Añade una tarea (presumiblemente ya completada) a la cima de la pila.
        """
        if isinstance(item, Task):
            # Usar el método 'push' estándar de la pila
            self.tasks.push(item)
        else:
            print("Error (CompletedTasks.addTask): Se intentó añadir un objeto que no es Task.")

    def editTask(self, task_id: int, attribute: str, newValue) -> bool:
        """
        Edita un atributo específico de una tarea completada, buscándola por su ID.
        Esta operación es O(n) porque puede requerir iterar la pila.

        Args:
            task_id: El ID numérico de la tarea a editar.
            attribute: El nombre del atributo a cambiar ("title", "description", "priority").
            newValue: El nuevo valor para el atributo.

        Returns:
            True si la tarea fue encontrada y editada, False en caso contrario.
        """
        edited = False
        # Iteramos directamente sobre la pila
        # La iteración será desde el fondo hacia la cima
        for task in self.tasks: # Equivalente a iterar self.tasks.get_items_list()
            if task.task_id == task_id:
                try:
                    match attribute:
                        case "title":
                            task.editTitle(str(newValue))
                            edited = True
                        case "description":
                            task.editDescription(str(newValue))
                            edited = True
                        case "priority":
                            # Permitir editar prioridad incluso en completadas según requerimiento
                            task.editPriority(int(newValue))
                            edited = True
                        case _:
                            print(f"Advertencia (CompletedTasks.editTask): Atributo '{attribute}' no editable.")
                            return False
                    break # Salir una vez encontrada y editada
                except (ValueError, TypeError) as e:
                     print(f"Error (CompletedTasks.editTask): Valor inválido '{newValue}' para atributo '{attribute}': {e}")
                     return False
                
        return edited

    def taskList(self) -> list[Task]:
        """
        Devuelve la lista de tareas completadas en orden LIFO (Last-In, First-Out),
        tal como se requiere para la visualización de la pila (la más reciente primero).
        """
        # Obtener la lista (que está en orden de inserción, fondo->cima)
        items_fifo = self.tasks.get_items_list()
        # Invertirla para obtener LIFO (cima->fondo)
        return items_fifo[::-1]

    def __len__(self) -> int:
        return len(self.tasks)