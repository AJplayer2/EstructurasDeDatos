# -*- coding: utf-8 -*-
"""
Módulo que define TaskListView, una vista personalizada para mostrar listas de tareas
con un efecto de desvanecimiento y manejo de selección.
"""
import sys
from PySide6.QtCore import (Qt, QModelIndex, QItemSelectionModel, Signal, Slot,
                            QObject, QAbstractListModel)
from PySide6.QtGui import QColor, QPainter, QPalette
from PySide6.QtWidgets import (QApplication, QListView, QStyledItemDelegate,
                               QStyleOptionViewItem, QWidget, QVBoxLayout,
                               QPushButton, QLabel) # Para el ejemplo

# --- Importación/Definición de TaskModel y Task ---
# Importar el TaskModel refactorizado (adaptador)
from src.GUIClasses.TaskModel import TaskModel
# Importar la Task refactorizada
from src.coreClasses.Task import Task

# --- Delegado para el Efecto de Desvanecimiento (Sin cambios respecto a la versión anterior) ---
class FadingItemDelegate(QStyledItemDelegate):
    """
    Un delegado que dibuja los ítems de una vista y aplica un efecto
    de desvanecimiento (transparencia) a los ítems en la parte inferior
    de la zona visible (viewport).
    """
    def __init__(self, fade_percentage: float = 0.25, parent: QObject | None = None):
        super().__init__(parent)
        self._fade_percentage = max(0.0, min(1.0, fade_percentage))

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        # 1. Dibujar base
        super().paint(painter, option, index)
        # 2. Calcular fade
        view = self.parent()
        if not isinstance(view, QListView): return
        viewport_rect = view.viewport().rect()
        item_rect = option.rect
        fade_height = viewport_rect.height() * self._fade_percentage
        fade_start_y = viewport_rect.height() - fade_height
        item_bottom_y = item_rect.bottom()
        opacity = 0.0
        if item_bottom_y > fade_start_y and item_rect.top() < viewport_rect.height() and fade_height > 0:
            overlap_bottom = min(item_bottom_y, viewport_rect.height())
            overlap_top = max(item_rect.top(), fade_start_y)
            overlap_height = overlap_bottom - overlap_top
            if overlap_height > 0:
                center_y_in_fade = (overlap_top + overlap_bottom) / 2.0 - fade_start_y
                opacity = center_y_in_fade / fade_height
                opacity = max(0.0, min(1.0, opacity))
        # 3. Dibujar overlay
        if opacity > 0.01:
            background_color = view.palette().color(QPalette.ColorRole.Base)
            overlay_color = QColor(background_color)
            overlay_color.setAlphaF(opacity)
            painter.save()
            painter.fillRect(item_rect, overlay_color)
            painter.restore()

# --- Vista Personalizada TaskListView ---
class TaskListView(QListView):
    """
    Una QListView personalizada diseñada para mostrar tareas (Task)
    usando un TaskModel y aplicando un efecto de desvanecimiento.

    Emite una señal 'taskSelected' cuando se selecciona una tarea.
    """
    # Señal emitida con el objeto Task seleccionado, o None si se deselecciona.
    taskSelected = Signal(object) # Usar 'Task' si la importación es segura, si no 'object'

    def __init__(self, parent: QWidget | None = None):
        """Inicializador de la vista."""
        super().__init__(parent)
        self.setItemDelegate(FadingItemDelegate(parent=self))
        # Conectar la señal interna de cambio de selección (si el selection model existe)
        # Es mejor conectar cuando se establece el modelo.

        # --- Estilos y Comportamiento ---
        self.setAlternatingRowColors(True)
        self.setDragDropMode(QListView.DragDropMode.NoDragDrop) # Deshabilitar drag & drop si no se usa
        self.setEditTriggers(QListView.EditTrigger.NoEditTriggers) # No permitir edición directa en la lista

    def setModel(self, model: QAbstractListModel | None) -> None:
        """Establece el modelo para la vista, (re)conectando señales de selección."""
        # Desconectar del modelo anterior si existe y estaba conectado
        current_model = self.model()
        if current_model and self.selectionModel():
            try:
                self.selectionModel().currentChanged.disconnect(self._handle_selection_changed)
            except (RuntimeError, TypeError): # Ignorar si no estaba conectado o hay error
                pass

        # Llamar al método base
        super().setModel(model)

        # Conectar al nuevo modelo si existe y tiene un selection model
        if model and self.selectionModel():
             try:
                 self.selectionModel().currentChanged.connect(self._handle_selection_changed)
             except Exception as e:
                 print(f"Error conectando currentChanged para nuevo modelo: {e}")


    @Slot(QModelIndex, QModelIndex)
    def _handle_selection_changed(self, current: QModelIndex, previous: QModelIndex) -> None:
        """Slot interno llamado cuando la selección cambia."""
        # pylint: disable=unused-argument
        task_object = None # Por defecto, no hay tarea seleccionada
        if current.isValid():
            # Obtener el modelo asociado a este índice (podría ser el proxy)
            model = current.model() # Usar el modelo del índice
            if model:
                # Obtener el objeto Task usando el rol definido en TaskModel
                # Es importante que TaskModel y PriorityFilterProxyModel usen el mismo rol
                task_object = model.data(current, TaskModel.TaskObjectRole) # O Qt.UserRole
                if not isinstance(task_object, Task):
                    # Si el rol devolvió algo inesperado, invalidarlo
                    print(f"TaskListView: Se obtuvo algo inesperado del modelo con UserRole: {type(task_object)}") # Debug
                    task_object = None
            else:
                 print("TaskListView: No se pudo obtener el modelo desde el índice.") # Debug

        # Emitir la señal con el objeto Task encontrado o None
        if task_object:
            print(f"TaskListView: Selección cambió, emitiendo taskSelected para: {task_object}") # Debug
        else:
            print("TaskListView: Selección borrada o tarea no obtenida, emitiendo None.") # Debug
        self.taskSelected.emit(task_object) # Emitir Task o None


    @Slot()
    def clearSelection(self) -> None:
        """Borra la selección actual en la vista."""
        if self.selectionModel():
            self.selectionModel().clearSelection()
            # Emitir señal con None al borrar explícitamente podría ser útil
            # self.taskSelected.emit(None)

    def selectTaskById(self, task_id: int) -> bool:
        """
        Selecciona un ítem en la lista basado en el ID numérico de la tarea.

        Args:
            task_id: El ID numérico de la tarea a seleccionar.

        Returns:
            True si la tarea fue encontrada y seleccionada, False en caso contrario.
        """
        model = self.model() # Este será el proxy model si se está usando uno
        if not model:
            print("TaskListView: No se puede seleccionar por ID, no hay modelo.")
            return False

        print(f"TaskListView: Buscando tarea con ID {task_id}...") # Debug
        for row in range(model.rowCount()):
            # Obtener el índice en el modelo (proxy)
            index = model.index(row, 0)
            # Obtener el objeto Task usando el rol
            task = model.data(index, TaskModel.TaskObjectRole) # O Qt.UserRole

            # Comparar con el task_id numérico estable
            if isinstance(task, Task) and task.task_id == task_id:
                # Encontrado: seleccionar la fila en la vista
                self.selectionModel().setCurrentIndex(index, QItemSelectionModel.SelectCurrent | QItemSelectionModel.Rows)
                self.scrollTo(index, QListView.ScrollHint.PositionAtCenter) # Asegurar visibilidad
                print(f"TaskListView: Tarea con ID {task_id} seleccionada en la fila {row} (índice proxy).") # Debug
                # No emitimos taskSelected aquí, _handle_selection_changed lo hará
                return True

        print(f"TaskListView: Tarea con ID {task_id} no encontrada en el modelo actual.") # Debug
        return False