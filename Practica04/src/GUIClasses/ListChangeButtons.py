# -*- coding: utf-8 -*-
"""
Módulo que define el widget ListChangeButtons para seleccionar
entre la vista de tareas pendientes y completadas.
"""
import sys
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton,
                               QButtonGroup, QHBoxLayout)

class ListChangeButtons(QWidget):
    """
    Widget con dos botones exclusivos ("PENDIENTES", "COMPLETADAS") para
    cambiar la vista de la lista de tareas.

    Señales:
        buttonPressed(int): Emitida cuando se presiona un botón,
                           enviando el ID asociado (1 para Pendientes, 2 para Completadas).
    """
    buttonPressed = Signal(int)

    # IDs para los botones
    PENDING_ID = 1
    COMPLETED_ID = 2

    def __init__(self, parent: QWidget | None = None):
        """Inicializador del widget."""
        super().__init__(parent)
        self.setObjectName("listChangeButtonsWidget") # Nombre de objeto para el widget
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura los widgets y el layout."""
        self.pending_button = QPushButton("PENDIENTES")
        self.pending_button.setObjectName("pendingViewButton") # Nombre de objeto para QSS/Testing
        self.pending_button.setCheckable(True)
        self.pending_button.setToolTip("Mostrar tareas pendientes")

        self.completed_button = QPushButton("COMPLETADAS")
        self.completed_button.setObjectName("completedViewButton") # Nombre de objeto para QSS/Testing
        self.completed_button.setCheckable(True)
        self.completed_button.setToolTip("Mostrar tareas completadas")

        # Grupo para asegurar exclusividad
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.pending_button, self.PENDING_ID)
        self.button_group.addButton(self.completed_button, self.COMPLETED_ID)
        self.button_group.setExclusive(True)

        # Conectar señal del grupo al slot interno (nombre corregido)
        self.button_group.idClicked.connect(self._on_button_clicked)

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) # Sin márgenes propios
        layout.setSpacing(6)
        layout.addWidget(self.pending_button)
        layout.addWidget(self.completed_button)
        layout.addStretch()

        # Establecer estado inicial (Pendientes seleccionado por defecto)
        self.pending_button.setChecked(True)
        # Emitir señal inicial para que la app principal sepa el estado inicial
        self.buttonPressed.emit(self.PENDING_ID) # O manejar esto en la app principal

    @Slot(int)
    def _on_button_clicked(self, button_id: int) -> None:
        """Slot interno que se activa cuando un botón del grupo es clickeado."""
        print(f"ListChangeButtons: Botón presionado ID: {button_id}") # Debug
        # Emitir la señal pública para que otros widgets reaccionen
        self.buttonPressed.emit(button_id)