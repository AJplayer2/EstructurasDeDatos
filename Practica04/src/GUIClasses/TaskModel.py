# -*- coding: utf-8 -*-
"""
Módulo que define el TaskModel, un adaptador Qt para los contenedores
de tareas (PendingTasks, CompletedTasks).
"""
import sys
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Slot, QObject
# Para el ejemplo __main__
from PySide6.QtWidgets import QApplication, QListView, QVBoxLayout, QWidget, QPushButton, QLabel

# --- Importación de Clases de Tareas y Contenedores ---
from src.coreClasses.Task import Task
from src.PendingTasks import PendingTasks
from src.CompletedTasks import CompletedTasks

# --- Implementación del Modelo TaskModel como Adaptador ---
class TaskModel(QAbstractListModel):
    """
    Modelo Qt que actúa como adaptador para un contenedor de tareas
    (como PendingTasks o CompletedTasks).

    Lee la lista de tareas del contenedor asociado a través de 'taskList()'
    y la almacena en una caché interna para uso de la vista.
    Notifica a las vistas para que se actualicen mediante 'refresh()'.
    """

    # Rol estándar de Qt para almacenar datos personalizados (el objeto Task completo).
    # Usar Qt.UserRole es común y evita definir constantes propias si no hay más roles.
    TaskObjectRole = Qt.ItemDataRole.UserRole

    def __init__(self, task_container: object | None = None, parent: QObject | None = None):
        """
        Inicializador del modelo.

        Args:
            task_container: La instancia de PendingTasks o CompletedTasks
                            que este modelo representará.
            parent: El objeto padre Qt (opcional).
        """
        super().__init__(parent)
        self._task_container = task_container
        self._tasks_cache: list[Task] = []
        print(f"TaskModel creado para contenedor: {type(self._task_container).__name__ if self._task_container else 'None'}")

    def set_task_container(self, container: object) -> None:
        """Asigna o cambia el contenedor de tareas (PendingTasks/CompletedTasks)."""
        print(f"TaskModel: Estableciendo contenedor: {type(container).__name__}")
        self._task_container = container
        # Es responsabilidad del código externo llamar a refresh() después.

    @Slot()
    def refresh(self) -> None:
        """
        Actualiza la caché interna del modelo leyendo desde el contenedor
        de tareas asociado y notifica a las vistas para que se actualicen.

        Debe ser llamado externamente cuando los datos en el contenedor cambien.
        """
        print(f"TaskModel: Iniciando refresh desde {type(self._task_container).__name__ if self._task_container else 'None'}")
        tasks = []
        if self._task_container and hasattr(self._task_container, 'taskList') and callable(self._task_container.taskList):
            try:
                tasks = self._task_container.taskList()
                if tasks is None: tasks = []
                # Verificar que los elementos sean Task (opcional, pero bueno para depurar)
                # tasks = [t for t in tasks if isinstance(t, Task)]
                print(f"TaskModel: Contenedor devolvió {len(tasks)} tareas.")
            except Exception as e:
                print(f"TaskModel: Error al llamar a taskList() del contenedor: {e}")
                tasks = []
        else:
            print(f"TaskModel: Contenedor no válido o sin método taskList(). Cache se vaciará.")

        # Notificar a las vistas ANTES de cambiar los datos internos
        self.beginResetModel()
        # Actualizar la caché interna
        self._tasks_cache = list(tasks) # Asegurar que es una lista
        # Notificar a las vistas DESPUÉS de cambiar los datos
        self.endResetModel()
        print(f"TaskModel: Refresh completo. Tamaño de caché: {len(self._tasks_cache)}")

    # --- Métodos Obligatorios Reimplementados (usan la caché) ---

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Devuelve el número de filas basado en la caché interna."""
        # Para modelos de lista, parent siempre es inválido.
        return len(self._tasks_cache) if not parent.isValid() else 0

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> object | None:
        """Devuelve los datos para un índice y rol específicos desde la caché."""
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return None # Índice inválido o fuera de rango

        try:
            task = self._tasks_cache[index.row()] # Obtener de la caché
        except IndexError:
             # Esto no debería ocurrir si rowCount y el índice son correctos, pero por si acaso
             print(f"TaskModel: Error INTERNO de índice en data() - Fila: {index.row()}, Tamaño caché: {len(self._tasks_cache)}")
             return None

        # Rol para mostrar texto en la vista
        if role == Qt.ItemDataRole.DisplayRole:
            # Usar el Task refactorizado con acceso directo a atributos
            prio_map = {3: "Urgente", 2: "Medio", 1: "Bajo"}
            prio_text = prio_map.get(task.priority, "N/A")
            return f"{task.title} ({prio_text})"

        # Rol para obtener el objeto Task completo (usando el rol estándar UserRole)
        if role == self.TaskObjectRole: # O Qt.UserRole
            return task

        # Otros roles (opcional)
        # if role == Qt.ToolTipRole:
        #     return task.description[:80] + ('...' if len(task.description) > 80 else '')

        return None # Rol no soportado

    # --- Método Auxiliar (opera sobre la caché) ---
    def getTaskFromRow(self, row: int) -> Task | None:
        """Obtiene el objeto Task en la fila especificada (desde la caché)."""
        if 0 <= row < self.rowCount():
             try:
                return self._tasks_cache[row]
             except IndexError:
                 # Podría ocurrir si el modelo se modifica entre llamadas, aunque refresh debería evitarlo
                 print(f"TaskModel: Error INTERNO de índice en getTaskFromRow() - Fila: {row}, Tamaño caché: {len(self._tasks_cache)}")
                 return None
        return None