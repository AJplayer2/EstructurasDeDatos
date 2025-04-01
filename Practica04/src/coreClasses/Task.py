# -*- coding: utf-8 -*-
class Task:
    """
    Representa una tarea individual con sus atributos.

    Atributos:
        task_id (int): Identificador numérico único e inmutable.
        title (str): Título de la tarea.
        description (str): Descripción detallada de la tarea.
        status (str): Estado actual ("Pendiente" o "Completada").
        priority (int): Nivel de prioridad (3: Urgente, 2: Medio, 1: Bajo).
        # created_at (datetime): Ejemplo de atributo adicional
    """
    # Definir constantes para estados y prioridades puede ser útil
    STATUS_PENDING = "Pendiente"
    STATUS_COMPLETED = "Completada"
    PRIORITY_URGENT = 3
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 1

    def __init__(self, task_id: int, title: str, description: str,
                 status: str = STATUS_PENDING, priority: int = PRIORITY_LOW):
        """
        Inicializa una nueva tarea.

        Args:
            task_id: El ID numérico único asignado a esta tarea.
            title: El título de la tarea.
            description: La descripción de la tarea.
            status: El estado inicial (por defecto "Pendiente").
            priority: La prioridad inicial (por defecto 1 - Bajo).
        """
        if not isinstance(task_id, int) or task_id <= 0:
            # Validar que el ID sea un entero positivo
            raise ValueError("task_id debe ser un entero positivo.")
        if not title:
             raise ValueError("El título no puede estar vacío.")

        self.task_id: int = task_id
        self.title: str = title
        self.description: str = description
        self.status: str = status
        self.priority: int = priority

    def changeStatus(self, newStatus: str) -> None:
        """Actualiza el estado de la tarea."""
        # Podrías añadir validación para asegurar que newStatus es válido
        if newStatus in [self.STATUS_PENDING, self.STATUS_COMPLETED]:
            self.status = newStatus
        else:
            print(f"Advertencia: Estado '{newStatus}' no reconocido.")

    def editTitle(self, newTitle: str) -> None:
        """Actualiza el título de la tarea."""
        if newTitle: # Evitar títulos vacíos
             self.title = newTitle
        else:
             print("Advertencia: El título no puede estar vacío.")


    def editDescription(self, newDescription: str = "") -> None:
        """Actualiza la descripción de la tarea."""
        self.description = newDescription

    def editPriority(self, newPriority: int) -> None:
        """Actualiza la prioridad de la tarea."""
        # Podrías añadir validación para asegurar que la prioridad es válida
        if newPriority in [self.PRIORITY_URGENT, self.PRIORITY_MEDIUM, self.PRIORITY_LOW]:
            self.priority = newPriority
        else:
            print(f"Advertencia: Prioridad '{newPriority}' no reconocida.")

    def to_dict(self) -> dict:
        """Convierte la tarea a un diccionario para serialización."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            # "created_at": self.created_at.isoformat() # Ejemplo
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Crea una instancia de Task desde un diccionario."""
        # Añadir validación de datos del diccionario si es necesario
        try:
            return cls(
                task_id=int(data['task_id']), # Asegurar que el ID es int
                title=data['title'],
                description=data['description'],
                status=data['status'],
                priority=int(data['priority']) # Asegurar que la prioridad es int
                # created_at=datetime.datetime.fromisoformat(data['created_at']) # Ejemplo
            )
        except KeyError as e:
            raise ValueError(f"Falta la clave requerida en los datos del diccionario: {e}")
        except ValueError as e:
             raise ValueError(f"Error al convertir datos del diccionario: {e}")


    def __repr__(self) -> str:
        """Representación útil para depuración."""
        return (f"Task(id={self.task_id}, title='{self.title}', "
                f"status='{self.status}', priority={self.priority})")

    def __eq__(self, other) -> bool:
         """Compara tareas basado en su ID único."""
         if not isinstance(other, Task):
             return NotImplemented
         return self.task_id == other.task_id

    def __hash__(self) -> int:
         """Permite usar tareas en sets o como claves de diccionario."""
         return hash(self.task_id)