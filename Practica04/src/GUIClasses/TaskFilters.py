# -*- coding: utf-8 -*-
"""
Módulo que define el widget TaskFilters para filtrar tareas por prioridad.
"""
import sys
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton,
                               QButtonGroup, QHBoxLayout)

class TaskFilters(QWidget):
    """
    Widget con botones exclusivos para filtrar tareas por prioridad
    (Todas, Urgente, Media, Baja).

    Señales:
        filterChanged(int): Emitida cuando se selecciona un filtro,
                            enviando el ID de prioridad asociado
                            (0: Todas, 3: Urgente, 2: Media, 1: Baja).
    """
    filterChanged = Signal(int) # Señal renombrada

    # IDs para los filtros
    FILTER_ALL_ID = 0
    FILTER_URGENT_ID = 3
    FILTER_MEDIUM_ID = 2
    FILTER_LOW_ID = 1

    def __init__(self, parent: QWidget | None = None):
        """Inicializador del widget de filtros."""
        super().__init__(parent)
        self.setObjectName("taskFiltersWidget")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura los widgets y el layout."""
        self.all_button = QPushButton("TODAS")
        self.all_button.setObjectName("filterAllButton")
        self.all_button.setCheckable(True)
        self.all_button.setToolTip("Mostrar todas las tareas")

        self.urgent_button = QPushButton("URGENTE")
        self.urgent_button.setObjectName("filterUrgentButton")
        self.urgent_button.setCheckable(True)
        self.urgent_button.setToolTip("Mostrar solo tareas urgentes (Prioridad 3)")

        self.medium_button = QPushButton("MEDIA")
        self.medium_button.setObjectName("filterMediumButton")
        self.medium_button.setCheckable(True)
        self.medium_button.setToolTip("Mostrar solo tareas de prioridad media (Prioridad 2)")

        self.low_button = QPushButton("BAJA")
        self.low_button.setObjectName("filterLowButton")
        self.low_button.setCheckable(True)
        self.low_button.setToolTip("Mostrar solo tareas de prioridad baja (Prioridad 1)")

        # Grupo para asegurar exclusividad
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.all_button, self.FILTER_ALL_ID)
        self.button_group.addButton(self.urgent_button, self.FILTER_URGENT_ID)
        self.button_group.addButton(self.medium_button, self.FILTER_MEDIUM_ID)
        self.button_group.addButton(self.low_button, self.FILTER_LOW_ID)
        self.button_group.setExclusive(True)

        # Conectar señal del grupo al slot interno (nombre corregido)
        self.button_group.idClicked.connect(self._on_filter_button_clicked)

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addWidget(self.all_button)
        layout.addWidget(self.urgent_button)
        layout.addWidget(self.medium_button)
        layout.addWidget(self.low_button)
        layout.addStretch()

        # Establecer estado inicial (Todas seleccionado por defecto)
        self.all_button.setChecked(True)
        # Emitir señal inicial si es necesario
        self.filterChanged.emit(self.FILTER_ALL_ID)

    @Slot(int)
    def _on_filter_button_clicked(self, filter_id: int) -> None:
        """Slot interno que se activa cuando un botón de filtro es clickeado."""
        print(f"TaskFilters: Filtro presionado ID: {filter_id}") # Debug
        # Emitir la señal pública renombrada
        self.filterChanged.emit(filter_id)