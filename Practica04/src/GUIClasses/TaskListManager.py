# -*- coding: utf-8 -*-
"""
Módulo que define el widget TaskListManager, responsable de gestionar
y mostrar las vistas de lista de tareas pendientes y completadas.
"""
import sys
from PySide6.QtCore import Signal, Slot, QObject, QSortFilterProxyModel, QAbstractListModel
from PySide6.QtWidgets import (QApplication, QWidget, QStackedLayout, QVBoxLayout,
                               QLabel, QPushButton) # Para el ejemplo

# --- Importaciones de Clases Personalizadas ---
# Importar la VISTA de lista personalizada
from src.GUIClasses.TaskListView import TaskListView
# Importar Task para type hinting en la señal
from src.coreClasses.Task import Task
# Importar TaskModel para chequeo de tipo
from src.GUIClasses.TaskModel import TaskModel
# Clases dummy para el ejemplo __main__ si las reales no están disponibles
from src.GUIClasses.ListChangeButtons import ListChangeButtons
from src.PendingTasks import PendingTasks
from src.CompletedTasks import CompletedTasks

# --- Widget Gestor de Listas (TaskListManager) ---
class TaskListManager(QWidget):
    """
    Widget que gestiona y muestra las vistas TaskListView para tareas
    pendientes y completadas usando un QStackedLayout.

    Permite cambiar entre vistas y retransmite la señal de selección
    de la vista activa.
    """
    # Señal retransmitida desde la TaskListView activa. Pasa el objeto Task o None.
    currentTaskSelected = Signal(object)

    def __init__(self, parent: QWidget | None = None):
        """Inicializador del gestor de listas."""
        super().__init__(parent)

        # --- Crear las Vistas de Lista Internas ---
        # Usar la clase TaskListView refactorizada
        self.pending_list_view = TaskListView(self)
        self.pending_list_view.setObjectName("pendingTaskListView")

        self.completed_list_view = TaskListView(self)
        self.completed_list_view.setObjectName("completedTaskListView")

        # --- Configurar el Layout Apilado ---
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.pending_list_view)
        self.stacked_layout.addWidget(self.completed_list_view)

        # --- Layout Contenedor ---
        # QStackedLayout necesita estar dentro de otro layout
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0) # Sin márgenes propios
        container_layout.addLayout(self.stacked_layout)

        # --- Conectar Señales Internas ---
        self.pending_list_view.taskSelected.connect(self._relay_task_selected)
        self.completed_list_view.taskSelected.connect(self._relay_task_selected)

        # Establecer la vista inicial por defecto (pendientes)
        self.stacked_layout.setCurrentWidget(self.pending_list_view)

    # --- Slots Públicos ---

    @Slot(int)
    def setCurrentView(self, view_id: int) -> None:
        """
        Cambia la vista de lista visible en el QStackedLayout.

        Args:
            view_id: 1 para pendientes (ID de ListChangeButtons),
                     2 para completadas (ID de ListChangeButtons).
        """
        print(f"TaskListManager: Recibido setCurrentView con ID: {view_id}") # Debug
        target_widget = None
        if view_id == 1: # Asumiendo 1 = Pendientes
            target_widget = self.pending_list_view
            view_name = "Pendientes"
        elif view_id == 2: # Asumiendo 2 = Completadas
            target_widget = self.completed_list_view
            view_name = "Completadas"
        else:
            print(f"TaskListManager: ID de vista no reconocido: {view_id}") # Debug
            return

        if self.stacked_layout.currentWidget() != target_widget:
            self.stacked_layout.setCurrentWidget(target_widget)
            print(f"TaskListManager: Cambiado a vista {view_name}.") # Debug
            target_widget.clearSelection()

    @Slot()
    def refreshModels(self) -> None:
        """
        Llama al método refresh() en los modelos *fuente* asociados a las vistas
        internas (si existen y tienen dicho método). Es seguro llamar aunque
        las vistas usen modelos proxy.
        """
        print("TaskListManager: Solicitando refresh de modelos fuente...") # Debug
        refreshed_count = 0
        for view in [self.pending_list_view, self.completed_list_view]:
            model = view.model() # Obtener el modelo asignado (puede ser proxy)
            source_model: QAbstractListModel | None = None

            # Determinar el modelo fuente
            if isinstance(model, QSortFilterProxyModel):
                source_model = model.sourceModel()
            elif isinstance(model, QAbstractListModel): # Si no es proxy, es el fuente
                source_model = model
            else:
                 print(f"TaskListManager: Vista {type(view).__name__} no tiene un modelo Qt válido.") # Debug

            # Verificar y llamar a refresh en el modelo fuente
            if source_model is not None and hasattr(source_model, 'refresh') and callable(source_model.refresh):
                try:
                    print(f"TaskListManager: Llamando refresh() en modelo fuente ({type(source_model).__name__}) de {type(view).__name__}") # Debug
                    source_model.refresh()
                    refreshed_count += 1
                except Exception as e:
                    print(f"TaskListManager: Error al llamar refresh() en el modelo fuente: {e}") # Debug
            elif source_model:
                 print(f"TaskListManager: Modelo fuente ({type(source_model).__name__}) no tiene método refresh() para {type(view).__name__}") # Debug

        print(f"TaskListManager: {refreshed_count} modelos fuente refrescados.") # Debug

    # --- Slots Internos / Privados ---

    @Slot(object) # Recibe Task o None
    def _relay_task_selected(self, task: Task | None) -> None:
        """
        Slot interno que recibe la señal 'taskSelected' de las TaskListView
        y la retransmite como 'currentTaskSelected' de este widget.
        """
        # Simplemente retransmitir lo que se recibió (sea Task o None)
        if task:
            print(f"TaskListManager: Retransmitiendo selección: {task}") # Debug
        else:
            print("TaskListManager: Retransmitiendo deselección (None).") # Debug
        self.currentTaskSelected.emit(task)

    # --- Métodos de Acceso (Útiles para la configuración externa) ---

    def getPendingListView(self) -> TaskListView:
        """Devuelve la instancia de la vista de lista de pendientes."""
        return self.pending_list_view

    def getCompletedListView(self) -> TaskListView:
        """Devuelve la instancia de la vista de lista de completadas."""
        return self.completed_list_view