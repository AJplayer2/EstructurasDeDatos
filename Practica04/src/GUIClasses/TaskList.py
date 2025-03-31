# -*- coding: utf-8 -*-
import sys
from PySide6.QtCore import (Qt, QModelIndex, QItemSelectionModel, Signal, Slot,
                            QObject, QAbstractListModel)
from PySide6.QtGui import QColor, QPainter, QPalette
from PySide6.QtWidgets import (QApplication, QListView, QStyledItemDelegate,
                               QStyleOptionViewItem, QWidget, QVBoxLayout,
                               QPushButton, QLabel) # Para el ejemplo

# --- Importación/Definición de TaskModel y Task ---
# Intenta importar las clases reales. Ajusta las rutas si es necesario.
try:
    from TaskModel import TaskModel # Asumiendo que guardaste el modelo anterior como task_model_adapter.py
    from src.coreClasses.Task import Task
    from src.PendingTasks import PendingTasks
except ImportError as e:
    print(f"ADVERTENCIA: Falló importación ({e}). Usando clases/modelo de ejemplo.")
    # Definiciones de ejemplo si las importaciones fallan
    class Task:
        def __init__(self, title="Dummy Task", description="...", status="Pendiente", ID="10"):
            self.title = title; self.description = description; self.status = status; self.ID = ID
            try: self.priority = int(ID[0]) if ID else 1
            except ValueError: self.priority = 1
        def __repr__(self): return f"Task(ID='{self.ID}', Title='{self.title}')"

    class TaskModel(QAbstractListModel): # Modelo de ejemplo mínimo
        TaskObjectRole = Qt.ItemDataRole.UserRole + 1
        def __init__(self, parent=None):
            super().__init__(parent); self._tasks = []
        def rowCount(self, parent=QModelIndex()): return len(self._tasks)
        def data(self, index, role=Qt.ItemDataRole.DisplayRole):
            if not index.isValid(): return None
            task = self._tasks[index.row()]
            if role == Qt.ItemDataRole.DisplayRole: return task.title
            if role == Qt.ItemDataRole.UserRole: return task
            return None
        def loadTasks(self, tasks):
            self.beginResetModel(); self._tasks = list(tasks); self.endResetModel()
        def getTask(self, row): return self._tasks[row] if 0 <= row < len(self._tasks) else None
        def refresh(self): self.beginResetModel(); self.endResetModel() # Simulación mínima

# --- Delegado para el Efecto de Desvanecimiento ---
class FadingItemDelegate(QStyledItemDelegate):
    """
    Un delegado que dibuja los ítems de una vista y aplica un efecto
    de desvanecimiento (transparencia) a los ítems en la parte inferior
    de la zona visible (viewport).
    """
    def __init__(self, fade_percentage: float = 0.25, parent: QObject | None = None):
        """
        Inicializador del delegado.

        Args:
            fade_percentage: Qué porción de la altura del viewport (desde abajo)
                             se usará para el desvanecimiento (ej. 0.25 para 25%).
            parent: El objeto padre Qt (normalmente la vista).
        """
        super().__init__(parent)
        # Asegurar que el porcentaje esté entre 0 y 1
        self._fade_percentage = max(0.0, min(1.0, fade_percentage))

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        """Dibuja el ítem y aplica el desvanecimiento si es necesario."""
        # 1. Dibujar el ítem base (texto, fondo seleccionado, etc.)
        # Llamamos a la implementación base para el dibujado estándar.
        super().paint(painter, option, index)

        # 2. Calcular si se debe aplicar desvanecimiento y con qué opacidad
        view = self.parent() # El padre debería ser la TaskListView
        if not isinstance(view, QListView):
            return # No hacer nada si no estamos en una QListView

        viewport_rect = view.viewport().rect()
        item_rect = option.rect

        # Calcular la zona de desvanecimiento en coordenadas del viewport
        fade_height = viewport_rect.height() * self._fade_percentage
        fade_start_y = viewport_rect.height() - fade_height

        item_bottom_y = item_rect.bottom()

        opacity = 0.0 # Opacidad del *overlay* de desvanecimiento (0 = sin overlay)

        if item_bottom_y > fade_start_y and item_rect.top() < viewport_rect.height() and fade_height > 0:
            # El ítem está (al menos parcialmente) en la zona de desvanecimiento

            # Calcular cuánto del ítem está DENTRO de la zona de fade
            overlap_bottom = min(item_bottom_y, viewport_rect.height())
            overlap_top = max(item_rect.top(), fade_start_y)
            overlap_height = overlap_bottom - overlap_top

            if overlap_height > 0:
                 # Calcular opacidad promedio basada en el centro del overlap
                center_y_in_fade = (overlap_top + overlap_bottom) / 2.0 - fade_start_y
                opacity = center_y_in_fade / fade_height
                opacity = max(0.0, min(1.0, opacity)) # Asegurar entre 0 y 1

        # 3. Dibujar el overlay de desvanecimiento si es necesario
        if opacity > 0.01: # Umbral pequeño para evitar dibujar overlays casi invisibles
            # Usar el color de fondo base de la paleta de la vista
            background_color = view.palette().color(QPalette.ColorRole.Base)
            overlay_color = QColor(background_color)
            # La opacidad del overlay va de 0 (arriba del fade) a 255 (abajo del fade)
            overlay_color.setAlphaF(opacity)

            painter.save() # Guardar estado del painter
            painter.fillRect(item_rect, overlay_color) # Dibujar rectángulo translúcido
            painter.restore() # Restaurar estado


# --- Vista Personalizada TaskListView ---
class TaskListView(QListView):
    """
    Una QListView personalizada diseñada para mostrar tareas (Task)
    usando un TaskModel y aplicando un efecto de desvanecimiento.

    Emite una señal 'taskSelected' cuando se selecciona una tarea.
    """
    # Señal emitida cuando se selecciona una tarea. Pasa el objeto Task.
    # Usar 'object' si la clase Task no está definida/importada aquí de forma fiable.
    taskSelected = Signal(object) # Cambiar 'object' a 'Task' si la importación es segura

    def __init__(self, parent: QWidget | None = None):
        """Inicializador de la vista."""
        super().__init__(parent)

        # Establecer el delegado personalizado para el efecto de desvanecimiento
        self.setItemDelegate(FadingItemDelegate(parent=self))

        # Conectar la señal interna de cambio de selección a nuestro slot
        if self.selectionModel(): # Asegurarse de que el modelo de selección existe
             self.selectionModel().currentChanged.connect(self._handle_selection_changed)

        # Otras configuraciones opcionales de QListView
        self.setAlternatingRowColors(True) # Mejora visual
        self.setUniformItemSizes(True) # Puede mejorar rendimiento si los ítems son iguales

    def setModel(self, model: TaskModel | QAbstractListModel | None) -> None:
        """Establece el modelo para la vista, reconectando señales de selección si es necesario."""
        # Desconectar del modelo anterior si existe
        if self.model() and self.selectionModel():
            try:
                self.selectionModel().currentChanged.disconnect(self._handle_selection_changed)
            except RuntimeError: # Ignorar si no estaba conectado
                pass

        # Llamar al método base para establecer el nuevo modelo
        super().setModel(model)

        # Conectar al nuevo modelo si existe
        if model and self.selectionModel():
             self.selectionModel().currentChanged.connect(self._handle_selection_changed)

    @Slot(QModelIndex, QModelIndex)
    def _handle_selection_changed(self, current: QModelIndex, previous: QModelIndex) -> None:
        """Slot interno llamado cuando la selección cambia."""
        # pylint: disable=unused-argument
        if current.isValid():
            model = self.model()
            if isinstance(model, TaskModel): # Verificar si es nuestro TaskModel esperado
                # Obtener el objeto Task usando el rol UserRole (o el rol personalizado)
                task_object = model.data(current, TaskModel.TaskObjectRole) # O Qt.UserRole
                if task_object:
                    # Emitir la señal personalizada con el objeto Task
                    print(f"TaskListView: Selección cambió, emitiendo taskSelected para: {task_object}") # Debug
                    self.taskSelected.emit(task_object)
                else:
                    print(f"TaskListView: Índice seleccionado válido, pero no se pudo obtener Task object (rol incorrecto?).") # Debug
            else:
                 print(f"TaskListView: Modelo no es TaskModel, no se puede emitir Task.") # Debug
        else:
            # Opcional: Emitir la señal con None si la selección se borra
            # self.taskSelected.emit(None)
            print("TaskListView: Selección borrada o índice inválido.") # Debug

    @Slot()
    def clearSelection(self) -> None:
        """Borra la selección actual en la vista."""
        if self.selectionModel():
            self.selectionModel().clearSelection()

    def selectTaskById(self, task_id: str) -> bool:
        """Selecciona un ítem en la lista basado en el ID de la tarea."""
        model = self.model()
        if not isinstance(model, TaskModel):
            print("TaskListView: No se puede seleccionar por ID, modelo no es TaskModel.")
            return False

        for row in range(model.rowCount()):
            index = model.index(row, 0)
            task = model.data(index, TaskModel.TaskObjectRole) # O Qt.UserRole
            if task and getattr(task, 'ID', None) == task_id:
                # Encontrado: seleccionar la fila
                self.selectionModel().setCurrentIndex(index, QItemSelectionModel.SelectCurrent | QItemSelectionModel.Rows)
                self.scrollTo(index) # Asegurarse de que el ítem sea visible
                print(f"TaskListView: Tarea con ID {task_id} seleccionada en la fila {row}.") # Debug
                return True

        print(f"TaskListView: Tarea con ID {task_id} no encontrada.") # Debug
        return False


# --- Ejemplo de Uso Básico ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear contenedor y modelo de ejemplo
    task_container = PendingTasks() # Usando la clase de ejemplo
    model = TaskModel(task_container)

    # Cargar tareas de ejemplo en el contenedor
    tasks_to_load = []
    for i in range(20):
        prio = (i % 3) + 1
        tasks_to_load.append(Task(title=f"Tarea {i+1}", ID=f"{prio}{i+1:02d}"))
    task_container.items = tasks_to_load # Carga directa para el ejemplo
    model.refresh() # Actualizar el modelo

    # Crear la vista personalizada
    task_list_view = TaskListView()
    task_list_view.setModel(model) # Asignar el modelo a la vista

    # Conectar la señal personalizada de la vista a un slot de ejemplo
    def on_task_selected(selected_task):
        if selected_task:
            print(f"\n--- Señal Recibida por la App Principal ---")
            print(f"Tarea seleccionada: ID={selected_task.ID}, Título='{selected_task.title}'")
            print(f"----------------------------------------\n")
        else:
            print("\n--- Selección Borrada ---\n")

    task_list_view.taskSelected.connect(on_task_selected)

    # Crear ventana de prueba
    window = QWidget()
    window.setWindowTitle("Prueba TaskListView con Desvanecimiento")
    layout = QVBoxLayout(window)
    layout.addWidget(QLabel("Lista de Tareas (con desvanecimiento abajo):"))
    layout.addWidget(task_list_view)

    # Botón para probar la selección por ID
    button_select = QPushButton("Seleccionar Tarea con ID '205'")
    button_select.clicked.connect(lambda: task_list_view.selectTaskById("205"))
    layout.addWidget(button_select)


    window.resize(400, 500)
    window.show()
    sys.exit(app.exec())
