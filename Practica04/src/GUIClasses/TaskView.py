import sys
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QTextEdit,
                               QComboBox, QVBoxLayout, QHBoxLayout,
                               QSizePolicy, QPushButton)

# Clase para el Widget de Detalles de Tarea
class TaskView(QWidget):
    # --- Señales Personalizadas ---
    # Señal emitida cuando el texto de la descripción cambia
    descriptionChanged = Signal(str)
    # Señal emitida cuando la prioridad cambia (emite el ID entero: 3, 2, o 1)
    priorityChanged = Signal(int)

    # --- Mapeo de Prioridad ---
    # Diccionario para mapear ID entero a texto descriptivo
    PRIORITY_MAP_INT_TO_STR = {
        3: "Urgente",
        2: "Medio",
        1: "Bajo"
    }
    # Diccionario para mapear texto descriptivo a ID entero (inverso)
    PRIORITY_MAP_STR_TO_INT = {v: k for k, v in PRIORITY_MAP_INT_TO_STR.items()}
    # Orden deseado para mostrar en el ComboBox
    PRIORITY_DISPLAY_ORDER = ["Urgente", "Medio", "Bajo"]


    def __init__(self, parent=None):
        super().__init__(parent)

        # --- Configuración Inicial del Widget ---
        self._block_signals = False # Bandera para evitar señales durante la carga inicial
        self._setup_ui()
        self._connect_signals()
        # Aplicar estilo para el borde
        self.setStyleSheet("""
            TaskDetailWidget {
                border: 1px solid #cccccc; /* Borde gris claro */
                border-radius: 5px;      /* Esquinas redondeadas */
                padding: 5px;            /* Espaciado interno */
            }
            QLabel#titleLabel { /* Estilo específico para el título */
                font-weight: bold;
                font-size: 14pt; /* Tamaño de fuente más grande */
                margin-bottom: 5px; /* Espacio debajo del título */
            }
        """)

    def _setup_ui(self):
        """Configura los elementos de la interfaz de usuario y los layouts."""
        # --- Crear Widgets ---
        self.title_label = QLabel("Título de la Tarea")
        self.title_label.setObjectName("titleLabel") # Para aplicar estilo QSS específico
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Centrar título

        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Descripción de la tarea...")
        # Permitir que el QTextEdit crezca verticalmente
        self.description_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.status_label = QLabel("Estado: Desconocido")
        self.priority_combo = QComboBox()

        # --- Poblar ComboBox de Prioridad ---
        # Añadir ítems usando texto y asociando el ID entero como userData
        for text in self.PRIORITY_DISPLAY_ORDER:
            priority_id = self.PRIORITY_MAP_STR_TO_INT[text]
            self.priority_combo.addItem(text, userData=priority_id)

        # --- Configurar Layouts ---
        # Layout principal vertical
        main_layout = QVBoxLayout(self) # Asignar layout directamente al widget

        # Layout horizontal para la parte inferior (status y prioridad)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch() # Añadir espacio flexible entre status y prioridad
        bottom_layout.addWidget(QLabel("Prioridad:")) # Etiqueta para el ComboBox
        bottom_layout.addWidget(self.priority_combo)

        # Añadir widgets al layout principal
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.description_edit)
        main_layout.addLayout(bottom_layout) # Añadir el layout horizontal inferior

        # No es necesario setFrameStyle si usamos QSS en el propio widget

    def _connect_signals(self):
        """Conecta las señales internas a los slots correspondientes."""
        # Conectar cambio de texto en descripción a nuestro slot
        self.description_edit.textChanged.connect(self._on_description_changed)
        # Conectar cambio de selección en prioridad a nuestro slot
        self.priority_combo.currentIndexChanged.connect(self._on_priority_changed)

    # --- Slots Internos ---
    @Slot()
    def _on_description_changed(self):
        """Slot llamado cuando el texto de descripción cambia."""
        if not self._block_signals: # Solo emitir si no estamos bloqueando señales
            new_description = self.description_edit.toPlainText()
            print(f"Detail Widget: Description changed, emitting signal.") # Debug
            self.descriptionChanged.emit(new_description)

    @Slot(int) # El índice no lo usamos directamente, pero es la señal
    def _on_priority_changed(self, index):
        """Slot llamado cuando la selección de prioridad cambia."""
        if not self._block_signals: # Solo emitir si no estamos bloqueando señales
            # Obtener el ID entero asociado con el ítem seleccionado
            selected_priority_id = self.priority_combo.currentData()
            if selected_priority_id is not None:
                print(f"Detail Widget: Priority changed to ID {selected_priority_id}, emitting signal.") # Debug
                self.priorityChanged.emit(selected_priority_id)

    # --- Método Público para Establecer Datos ---
    def setTaskData(self, title: str, description: str, status: str, priority: int):
        """
        Establece los datos de la tarea que se mostrarán en el widget.

        Args:
            title: El título de la tarea.
            description: La descripción de la tarea.
            status: El estado actual de la tarea (ej: "Pendiente", "Completada").
            priority: La prioridad como entero (3: Urgente, 2: Medio, 1: Bajo).
        """
        # Bloquear señales temporalmente para evitar emisiones durante la carga
        self._block_signals = True
        print(f"Detail Widget: Setting data - Title: {title}, PrioID: {priority}") # Debug

        self.title_label.setText(title if title else "Sin Título")
        self.description_edit.setText(description if description else "")
        self.status_label.setText(f"Estado: {status}" if status else "Estado: Desconocido")

        # Buscar el índice en el ComboBox que corresponde a la prioridad dada
        priority_text = self.PRIORITY_MAP_INT_TO_STR.get(priority, "Bajo") # Default a Bajo si no se encuentra
        index_to_select = self.priority_combo.findText(priority_text)

        if index_to_select != -1:
            self.priority_combo.setCurrentIndex(index_to_select)
        else:
             # Si la prioridad no es válida, seleccionar el último (Bajo por defecto)
             self.priority_combo.setCurrentIndex(self.priority_combo.count() - 1)

        # Desbloquear señales después de actualizar la UI
        self._block_signals = False
        print(f"Detail Widget: Data set. Signals unblocked.") # Debug

# --- Ejemplo de Uso ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear una ventana principal para probar el widget
    main_window = QWidget()
    main_window.setWindowTitle("Prueba TaskDetailWidget")
    layout = QVBoxLayout(main_window)

    # Crear instancia del widget de detalles
    task_detail = TaskView()

    # --- Conectar Señales del Widget de Detalles ---
    # Conectar la señal de cambio de descripción a una función lambda (o un slot)
    task_detail.descriptionChanged.connect(
        lambda desc: print(f"--- Main Window received description: {desc[:50]}...")
    )
    # Conectar la señal de cambio de prioridad a una función lambda (o un slot)
    task_detail.priorityChanged.connect(
        lambda prio_id: print(f"--- Main Window received new priority ID: {prio_id}")
    )

    # Añadir el widget de detalles al layout de la ventana principal
    layout.addWidget(task_detail)

    # --- Simular Carga de Datos ---
    # Datos de ejemplo para una tarea
    ejemplo_titulo = "Preparar informe semanal"
    ejemplo_desc = "Recopilar datos de ventas y marketing.\nGenerar gráficos.\nEscribir resumen ejecutivo."
    ejemplo_status = "Pendiente"
    ejemplo_prioridad = 3 # Urgente

    # Establecer los datos en el widget
    task_detail.setTaskData(ejemplo_titulo, ejemplo_desc, ejemplo_status, ejemplo_prioridad)

    # Botón para simular carga de otra tarea
    load_button = QPushButton("Cargar Otra Tarea (Prioridad Media)")
    def load_another_task():
        task_detail.setTaskData("Revisar correo", "Leer y responder emails importantes.", "Pendiente", 2)
    load_button.clicked.connect(load_another_task)
    layout.addWidget(load_button)


    main_window.resize(400, 300) # Tamaño inicial razonable
    main_window.show()
    sys.exit(app.exec())