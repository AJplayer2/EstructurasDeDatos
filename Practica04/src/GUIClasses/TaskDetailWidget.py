# -*- coding: utf-8 -*-
"""
Módulo que define el widget TaskDetailWidget para mostrar y editar
los detalles de una tarea seleccionada.
"""
import sys
from PySide6.QtCore import Qt, Signal, Slot, QObject
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QTextEdit, QFrame,
                               QComboBox, QVBoxLayout, QHBoxLayout, QSizePolicy,
                               QPushButton) # Para el ejemplo

# --- Importación de Clases Necesarias ---
from src.coreClasses.Task import Task
# --- Clase TaskDetailWidget ---
class TaskDetailWidget(QWidget):
    """
    Widget para mostrar y editar los detalles de una tarea.

    Emite señales cuando la descripción o la prioridad son modificadas por el usuario,
    incluyendo el ID de la tarea afectada.
    """
    # --- Señales Personalizadas (incluyen task_id) ---
    descriptionChanged = Signal(int, str) # task_id, nueva_descripcion
    priorityChanged = Signal(int, int)    # task_id, nuevo_id_prioridad

    # --- Mapeo de Prioridad (Constantes) ---
    PRIORITY_MAP_INT_TO_STR = { Task.PRIORITY_URGENT: "Urgente", Task.PRIORITY_MEDIUM: "Medio", Task.PRIORITY_LOW: "Bajo" }
    PRIORITY_MAP_STR_TO_INT = {v: k for k, v in PRIORITY_MAP_INT_TO_STR.items()}
    PRIORITY_DISPLAY_ORDER = ["Urgente", "Medio", "Bajo"] # Orden en ComboBox

    def __init__(self, parent: QWidget | None = None):
        """Inicializador del widget de detalles."""
        super().__init__(parent)

        # --- Estado Interno ---
        self._block_signals: bool = False # Para evitar señales durante carga/limpieza
        self._current_task_id: int | None = None # ID de la tarea actualmente mostrada

        # --- Configuración UI ---
        self._setup_ui()
        self._connect_signals()
        self.clear() # Empezar con el widget limpio y deshabilitado

    def _setup_ui(self) -> None:
        """Configura los elementos de la interfaz de usuario y los layouts."""
        # --- Crear Widgets ---
        self.title_label = QLabel("Seleccione una tarea") # Texto inicial
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True) # Permitir que el título ocupe varias líneas si es largo

        self.description_edit = QTextEdit()
        self.description_edit.setObjectName("descriptionEdit")
        self.description_edit.setPlaceholderText("Descripción...")
        self.description_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.status_label = QLabel("Estado:")
        self.status_label.setObjectName("statusLabel")

        self.priority_combo = QComboBox()
        self.priority_combo.setObjectName("priorityCombo")
        # Poblar ComboBox usando texto y asociando ID entero como userData
        for text in self.PRIORITY_DISPLAY_ORDER:
            priority_id = self.PRIORITY_MAP_STR_TO_INT.get(text, Task.PRIORITY_LOW) # Default a Bajo
            self.priority_combo.addItem(text, userData=priority_id)

        # --- Configurar Layouts ---
        main_layout = QVBoxLayout(self) # Layout principal vertical para este widget

        bottom_layout = QHBoxLayout() # Layout para la fila inferior
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(QLabel("Prioridad:")) # Etiqueta descriptiva
        bottom_layout.addWidget(self.priority_combo)

        # Añadir widgets al layout principal
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.description_edit, stretch=1) # Darle más espacio vertical
        main_layout.addLayout(bottom_layout)

    def _connect_signals(self) -> None:
        """Conecta las señales internas de los widgets a los slots."""
        self.description_edit.textChanged.connect(self._on_description_changed)
        self.priority_combo.currentIndexChanged.connect(self._on_priority_changed)

    # --- Slots Internos ---
    @Slot()
    def _on_description_changed(self) -> None:
        """Slot llamado cuando el texto de descripción cambia."""
        # Solo emitir si no estamos bloqueando señales Y hay una tarea cargada
        if not self._block_signals and self._current_task_id is not None:
            new_description = self.description_edit.toPlainText()
            print(f"DetailWidget: Description changed for task {self._current_task_id}, emitting signal.") # Debug
            self.descriptionChanged.emit(self._current_task_id, new_description)

    @Slot(int) # index no se usa, pero es parte de la señal
    def _on_priority_changed(self, index: int) -> None:
        """Slot llamado cuando la selección de prioridad cambia."""
         # Solo emitir si no estamos bloqueando señales Y hay una tarea cargada
        if not self._block_signals and self._current_task_id is not None:
            selected_priority_id = self.priority_combo.currentData() # Obtener el ID (int)
            if selected_priority_id is not None:
                print(f"DetailWidget: Priority changed for task {self._current_task_id} to ID {selected_priority_id}, emitting signal.") # Debug
                self.priorityChanged.emit(self._current_task_id, selected_priority_id)

    # --- Métodos Públicos ---
    @Slot()
    def clear(self) -> None:
        """Limpia la vista de detalles y deshabilita la edición."""
        self._block_signals = True # Bloquear señales durante la limpieza

        self._current_task_id = None
        self.title_label.setText("Seleccione una tarea")
        self.description_edit.setPlainText("")
        self.status_label.setText("Estado:")
        # Seleccionar un índice por defecto o inválido en el ComboBox
        self.priority_combo.setCurrentIndex(-1) # -1 usualmente no selecciona nada

        # Deshabilitar edición
        self.description_edit.setEnabled(False)
        self.priority_combo.setEnabled(False)
        self.title_label.setEnabled(False) # También deshabilitar etiquetas visualmente
        self.status_label.setEnabled(False)

        self._block_signals = False
        print("DetailWidget: Cleared and disabled.") # Debug

    @Slot(Task) # Aceptar un objeto Task
    def setTaskData(self, task: Task | None) -> None:
        """
        Establece los datos de la tarea que se mostrarán en el widget.
        Si task es None, limpia la vista.

        Args:
            task: El objeto Task a mostrar, o None para limpiar.
        """
        self._block_signals = True # Bloquear señales durante la carga/actualización

        if task is None or not isinstance(task, Task):
            self.clear() # Limpiar si no hay tarea válida
            self._block_signals = False
            return

        # Tenemos una tarea válida, actualizar campos
        self._current_task_id = task.task_id # Guardar el ID numérico
        print(f"DetailWidget: Setting data for Task ID: {self._current_task_id}") # Debug

        self.title_label.setText(task.title)
        self.description_edit.setPlainText(task.description)
        self.status_label.setText(f"Estado: {task.status}")

        # Buscar y seleccionar la prioridad en el ComboBox
        priority_text = self.PRIORITY_MAP_INT_TO_STR.get(task.priority)
        if priority_text:
            index_to_select = self.priority_combo.findText(priority_text)
            self.priority_combo.setCurrentIndex(index_to_select)
        else:
            self.priority_combo.setCurrentIndex(-1) # Prioridad no encontrada

        # Habilitar edición (solo si la tarea no está completada, según requerimiento?)
        # Requerimiento: Pendientes y Completadas pueden editar Desc/Prio
        can_edit = True # Ajustar si las completadas no pudieran editarse
        self.description_edit.setEnabled(can_edit)
        self.priority_combo.setEnabled(can_edit)
        self.title_label.setEnabled(True)
        self.status_label.setEnabled(True)

        self._block_signals = False
        print(f"DetailWidget: Data set for Task ID {self._current_task_id}. Editing enabled: {can_edit}") # Debug