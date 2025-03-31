# -*- coding: utf-8 -*-
"""
Módulo que define un QSortFilterProxyModel para filtrar tareas por prioridad.
"""
from PySide6.QtCore import QSortFilterProxyModel, QModelIndex, Slot, Qt, QObject

# --- Importación de Clases Necesarias ---
# Intenta importar las clases reales. Ajusta las rutas si es necesario.
# Es crucial que TaskModel defina TaskObjectRole consistentemente o usar Qt.UserRole.
try:
    # Asumiendo que TaskModel está en task_model_adapter.py o similar
    from TaskModel import TaskModel
    # Asumiendo que Task está en src.coreClasses.Task
    from src.coreClasses.Task import Task
except ImportError as e:
    print(f"ADVERTENCIA (ProxyModel): Falló importación ({e}). Usando definiciones de ejemplo.")
    # Clases de ejemplo si la importación falla
    class Task:
        def __init__(self, priority=0, title="Dummy"): self.priority = priority; self.title = title
        def __repr__(self): return f"Task(Prio={self.priority}, Title='{self.title}')"
    class TaskModel: # Dummy mínimo para que el proxy funcione
        TaskObjectRole = Qt.ItemDataRole.UserRole + 1 # Debe coincidir con el TaskModel real
        def data(self, index, role): return None # Implementación mínima
        def index(self, row, col, parent): return QModelIndex() # Implementación mínima

# --- Clase PriorityFilterProxyModel ---
class PriorityFilterProxyModel(QSortFilterProxyModel):
    """
    Proxy model que filtra un modelo fuente (TaskModel) basado en un ID de prioridad.

    Acepta filas si la prioridad de la tarea coincide con el filtro establecido,
    o si el filtro es 0 (mostrar todas).
    """
    def __init__(self, parent: QObject | None = None):
        """Inicializador del proxy model."""
        super().__init__(parent)
        self._filter_priority_id = 0 # Filtro inicial: 0 = Mostrar todas las tareas

    @Slot(int)
    def setPriorityFilter(self, priority_id: int) -> None:
        """
        Establece el ID de prioridad para filtrar.

        Args:
            priority_id: El ID de prioridad (1, 2, 3) o 0 para mostrar todas.
        """
        # Solo invalidar si el filtro realmente cambia
        if self._filter_priority_id != priority_id:
            print(f"ProxyFilter: Estableciendo filtro de prioridad a ID: {priority_id}") # Debug
            self._filter_priority_id = priority_id
            # Forzar la reevaluación del filtro en todas las filas
            self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        Determina si una fila del modelo fuente debe ser incluida en el modelo proxy.

        Args:
            source_row: El índice de la fila en el modelo fuente.
            source_parent: El índice del padre en el modelo fuente (usualmente inválido para listas).

        Returns:
            True si la fila pasa el filtro, False en caso contrario.
        """
        # Si el filtro es 0 ("ALL"), siempre se acepta la fila
        if self._filter_priority_id == 0:
            return True

        # Obtener el modelo fuente
        source_model = self.sourceModel()
        if not source_model:
            return False # No hay modelo fuente

        # Obtener el índice de la fila/columna 0 en el modelo fuente
        source_index = source_model.index(source_row, 0, source_parent)
        if not source_index.isValid():
            return False # Índice fuente inválido

        # Obtener el objeto Task completo desde el modelo fuente
        # Usando el rol definido en TaskModel (TaskObjectRole o UserRole)
        task = source_model.data(source_index, TaskModel.TaskObjectRole) # O Qt.UserRole

        # Verificar si obtuvimos un objeto Task y si tiene el atributo 'priority'
        if task and hasattr(task, 'priority'):
            # Comparar la prioridad de la tarea con el filtro activo
            print(f"ProxyFilter: Row {source_row}, TaskPrio={task.priority}, Filter={self._filter_priority_id}") # Debug detallado
            return task.priority == self._filter_priority_id
        else:
            # Si no se pudo obtener la tarea o su prioridad, se rechaza la fila
            print(f"ProxyFilter: Rechazando fila fuente {source_row} (Task o prioridad no encontrada)") # Debug
            return False