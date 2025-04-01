# -*- coding: utf-8 -*-
"""
Módulo para gestionar la colección de tareas pendientes usando una cola.
"""
# Importar Task refactorizada y CythonQueue renombrada como Queue

from src.coreClasses.Task import Task
# Importar la cola optimizada con Cython
from src.coreClasses.queue_cython import CythonQueue as Queue

class PendingTasks:
    """
    Gestiona la colección de tareas pendientes utilizando una implementación
    de Cola (Queue) optimizada con Cython.
    """
    def __init__(self):
        """Inicializa el contenedor de tareas pendientes con una cola vacía."""
        self.tasks: Queue[Task] = Queue() # Usar la CythonQueue importada

    def addTask(self, item: Task) -> None:
        """Añade una nueva tarea pendiente a la cola."""
        task=Task(101,'Title','desc','Pendiente',1)
        if isinstance(item, Task):
            self.tasks.enqueue(item)
        else:
            print(f"Error (PendingTasks.addTask): Se intentó añadir un objeto que no es Task. El objeto es de tipo {type(item)} y se esperaba uno de tipo {type(task)}")

    def completeTask(self) -> Task | None:
        """
        Extrae la siguiente tarea pendiente de la cola (FIFO),
        marca su estado como completado y la devuelve.
        Devuelve None si la cola está vacía.
        """
        if not self.tasks.isEmpty():
            try:
                completedTask = self.tasks.dequeue()
                # Usar la constante definida en Task (si existe)
                completedTask.changeStatus(Task.STATUS_COMPLETED)
                return completedTask
            except IndexError:
                # Aunque isEmpty() se chequea, dequeue podría fallar teóricamente
                print("Error (PendingTasks.completeTask): Dequeue falló inesperadamente.")
                return None
        return None # La cola está vacía

    def removeTask(self, task_to_remove: Task) -> bool:
        """
        Elimina una tarea específica de la cola.
        Esta operación es O(n) porque requiere reconstruir la cola interna.

        Args:
            task_to_remove: La instancia de la tarea a eliminar (se usa su task_id).

        Returns:
            True si la tarea fue encontrada y eliminada, False en caso contrario.
        """
        if not isinstance(task_to_remove, Task):
            return False

        found = False
        # Obtener todos los items actuales
        current_items = self.tasks.get_items_list()
        # Crear una nueva cola temporal (o limpiar la actual y re-llenar)
        new_queue = Queue()
        for task in current_items:
            # Comparar por ID (asumiendo que Task implementa __eq__ basado en task_id)
            if task == task_to_remove: # O usar task.task_id == task_to_remove.task_id
                found = True
            else:
                # Añadir solo las tareas que NO son la que queremos eliminar
                new_queue.enqueue(task)

        # Reemplazar la cola antigua con la nueva
        self.tasks = new_queue
        return found

    def editTask(self, task_id: int, attribute: str, newValue) -> bool:
        """
        Edita un atributo específico de una tarea pendiente, buscándola por su ID.
        Esta operación es O(n) porque puede requerir iterar la cola.

        Args:
            task_id: El ID numérico de la tarea a editar.
            attribute: El nombre del atributo a cambiar ("title", "description", "priority").
            newValue: El nuevo valor para el atributo.

        Returns:
            True si la tarea fue encontrada y editada, False en caso contrario.
        """
        edited = False

        # Iteramos directamente sobre la cola (asumiendo que CythonQueue soporta __iter__)
        for task in self.tasks:
            if task.task_id == task_id:
                try:
                    match attribute:
                        case "title":
                            task.editTitle(str(newValue)) # Asegurar tipo
                            edited = True
                        case "description":
                            task.editDescription(str(newValue)) # Asegurar tipo
                            edited = True
                        case "priority":
                            task.editPriority(int(newValue)) # Asegurar tipo
                            edited = True
                        case _:
                            print(f"Advertencia (PendingTasks.editTask): Atributo '{attribute}' no editable.")
                            return False # Atributo no válido
                    # Si encontramos y editamos, podemos salir del bucle
                    break
                except (ValueError, TypeError) as e:
                     print(f"Error (PendingTasks.editTask): Valor inválido '{newValue}' para atributo '{attribute}': {e}")
                     return False # Error en la conversión de tipo o valor

        return edited

    def taskList(self) -> list[Task]:
        """
        Devuelve la lista de tareas pendientes en su orden actual FIFO (First-In, First-Out).
        La ordenación para visualización (ej. por prioridad) debe hacerse
        en la capa de Modelo/Vista (ej. usando QSortFilterProxyModel).
        """
        # Devuelve una copia de la lista interna de la cola
        return self.tasks.get_items_list()

    def __len__(self) -> int:
        return self.tasks.size()

