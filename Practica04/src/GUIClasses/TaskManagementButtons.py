# -*- coding: utf-8 -*-
"""
Módulo que define el widget TaskManagementButtons, que contiene
los botones de acción principales (Add, Delete, Complete, Save, Load).
"""
import sys
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QSizePolicy

class TaskManagementButtons(QWidget):
    """
    Widget que agrupa los botones de acción principales para gestionar tareas.

    Señales:
        addTaskClicked: Emitida cuando se presiona el botón 'AÑADIR'.
        deleteTaskClicked: Emitida cuando se presiona el botón 'ELIMINAR'.
        completeTaskClicked: Emitida cuando se presiona el botón 'COMPLETAR'.
        saveTasksClicked: Emitida cuando se presiona el botón 'GUARDAR'.
        loadTasksClicked: Emitida cuando se presiona el botón 'CARGAR'.
    """
    # Definir señales para cada acción
    addTaskClicked = Signal()
    deleteTaskClicked = Signal()
    completeTaskClicked = Signal()
    saveTasksClicked = Signal()
    loadTasksClicked = Signal()

    def __init__(self, parent: QWidget | None = None):
        """Inicializador del widget."""
        super().__init__(parent)
        self.setObjectName("taskManagementButtonsWidget")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura los widgets y el layout."""
        # Crear los botones
        self.complete_button = QPushButton("COMPLETAR")
        self.complete_button.setObjectName("completeButton")
        self.complete_button.setToolTip("Marcar la siguiente tarea pendiente como completada")

        self.delete_button = QPushButton("ELIMINAR")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.setToolTip("Eliminar la tarea pendiente seleccionada")

        self.add_button = QPushButton("AÑADIR")
        self.add_button.setObjectName("addButton")
        self.add_button.setToolTip("Añadir una nueva tarea pendiente")

        self.save_button = QPushButton("GUARDAR")
        self.save_button.setObjectName("saveButton")
        self.save_button.setToolTip("Guardar todas las tareas en el archivo")

        self.load_button = QPushButton("CARGAR")
        self.load_button.setObjectName("loadButton")
        self.load_button.setToolTip("Cargar tareas desde el archivo")

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Añadir en el orden visual deseado 
        layout.addWidget(self.complete_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.add_button)
        layout.addStretch(1) # Espacio flexible que empuja Save/Load a la derecha
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        # Conectar el clic de cada botón a la emisión de su señal respectiva
        self.complete_button.clicked.connect(self.completeTaskClicked.emit)
        self.delete_button.clicked.connect(self.deleteTaskClicked.emit)
        self.add_button.clicked.connect(self.addTaskClicked.emit)
        self.save_button.clicked.connect(self.saveTasksClicked.emit)
        self.load_button.clicked.connect(self.loadTasksClicked.emit)

    @Slot(bool)
    def enableCompleteButton(self, enabled: bool):
        """Habilita o deshabilita el botón COMPLETAR."""
        self.complete_button.setEnabled(enabled)

    @Slot(bool)
    def enableDeleteButton(self, enabled: bool):
        """Habilita o deshabilita el botón ELIMINAR."""
        self.delete_button.setEnabled(enabled)

    @Slot(bool)
    def enableAddButton(self, enabled: bool):
        """Habilita o deshabilita el botón AÑADIR."""
        self.add_button.setEnabled(enabled)