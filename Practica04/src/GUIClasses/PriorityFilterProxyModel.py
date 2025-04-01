# -*- coding: utf-8 -*-
"""
Módulo que define un QSortFilterProxyModel para filtrar tareas por prioridad.
"""
from PySide6.QtCore import QSortFilterProxyModel, QModelIndex, Slot, Qt, QObject

# --- Importación de Clases Necesarias ---
# Importar TaskModel para acceder a TaskObjectRole y para type hints
from src.GUIClasses.TaskModel import TaskModel # O el nombre de tu archivo TaskModel
# Importar Task para type hints y acceso a atributos
from src.coreClasses.Task import Task

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
        self._filter_priority_id = 0 # Filtro inicial: 0 = Mostrar todas

    @Slot(int)
    def setPriorityFilter(self, priority_id: int) -> None:
        """
        Establece el ID de prioridad para filtrar (0 para mostrar todas).
        """
        filter_id = int(priority_id) # Asegurarse de que es entero
        if self._filter_priority_id != filter_id:
            print(f"ProxyFilter: Estableciendo filtro de prioridad a ID: {filter_id}") # Debug
            self._filter_priority_id = filter_id
            # Forzar la reevaluación del filtro
            self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        Determina si una fila del modelo fuente debe ser incluida.
        """
        # Si el filtro es "ALL" (ID 0), aceptar siempre
        if self._filter_priority_id == 0:
            return True

        # Obtener el modelo fuente
        source_model = self.sourceModel()
        # Verificar que el modelo fuente existe y es del tipo esperado (opcional)
        if not isinstance(source_model, TaskModel): # O QAbstractListModel si es más genérico
             print("ProxyFilter: Modelo fuente no es TaskModel o no existe.") # Debug
             return False # No se puede filtrar sin el modelo fuente correcto

        # Obtener el índice fuente
        source_index = source_model.index(source_row, 0, source_parent)
        if not source_index.isValid():
            return False # Índice fuente inválido

        # Obtener el objeto Task usando el rol definido en TaskModel
        # Es crucial que TaskModel.TaskObjectRole sea el rol correcto (o usar Qt.UserRole)
        task = source_model.data(source_index, TaskModel.TaskObjectRole)

        # Verificar si obtuvimos un objeto Task y comparar su prioridad
        # Usar acceso directo al atributo 'priority' de la Task refactorizada
        if isinstance(task, Task):
            print(f"ProxyFilter: Row {source_row}, TaskPrio={task.priority}, Filter={self._filter_priority_id}") # Debug detallado
            return task.priority == self._filter_priority_id
        else:
            # No se pudo obtener un objeto Task válido
            print(f"ProxyFilter: Rechazando fila fuente {source_row} (No se obtuvo Task)") # Debug
            return False