# -*- coding: utf-8 -*-
import sys
from PySide6.QtCore import Signal, Slot, QObject, QSortFilterProxyModel
from PySide6.QtWidgets import (QApplication, QWidget, QStackedLayout, QVBoxLayout,
                               QLabel, QPushButton) # Para el ejemplo

# --- Importaciones de Clases Personalizadas ---
# Intenta importar las clases reales. Ajusta las rutas según tu estructura.
try:
    # Asumiendo que TaskView está en un archivo TaskView.py
    from TaskView import TaskView
    # Asumiendo que Task está definido donde corresponde
    from src.coreClasses.Task import Task
    # Para type hinting y ejemplo, podríamos necesitar ListChangeButtons
    from ListChangeButtons import ListChangeButtons # Asumiendo archivo ListChangeButtons.py
    # Y el modelo
    from TaskModel import TaskModel
    # Y PendingTasks y CompletedTasks
    from src.CompletedTasks import CompletedTasks
    from src.PendingTasks import PendingTasks
except ImportError as e:
    print(f"ADVERTENCIA: Falló importación ({e}). Usando clases de ejemplo.")
    # Clases de ejemplo si las importaciones fallan
    from PySide6.QtWidgets import QListView # Usar QListView base si TaskView falla
    class TaskView(QListView):
        def __init__(self): super().__init__()
    class Task:
        def __init__(self, title="Dummy Task", ID="00"): self.title = title; self.ID = ID
        def __repr__(self): return f"Task(ID='{self.ID}', Title='{self.title}')"
    class ListChangeButtons(QWidget): # Dummy
        buttonPressed = Signal(int)
    class TaskModel: # Dummy
        def refresh(self): print("DummyModel: refresh called")
    class QStackedLayout: # Dummy simple (solo para que el código no falle)
        def __init__(self): self._widgets = []; self._current_widget = None
        def addWidget(self, w): self._widgets.append(w); return len(self._widgets) - 1
        def setCurrentWidget(self, w): self._current_widget = w; print(f"DummyStackedLayout: Set current to {w}")
        # Implementación mínima para el ejemplo
    class PendingTasks: # Clase de ejemplo
        def __init__(self): self.items = []
        def taskList(self): return sorted(self.items, key=lambda x: x.priority, reverse=True)
        def addTask(self, task): self.items.append(task) # Solo para prueba

    class CompletedTasks: # Clase de ejemplo
        def __init__(self): self.items = []
        def taskList(self): return list(self.items)
        def addTask(self, task): self.items.append(task) # Solo para prueba


# --- Widget Gestor de Listas (TaskListManager) ---
class TaskListManager(QWidget):
    """
    Widget que gestiona y muestra las vistas de lista de tareas
    (pendientes y completadas) usando un QStackedLayout.

    Cambia la vista activa basándose en señales externas y retransmite
    la selección de tarea de la vista activa.
    """
    # Señal retransmitida desde la TaskView activa. Pasa el objeto Task.
    currentTaskSelected = Signal(object) # Usar Signal(Task) si la importación es segura

    def __init__(self, parent: QWidget | None = None):
        """Inicializador del gestor de listas."""
        super().__init__(parent)

        # --- Crear las Vistas de Lista Internas ---
        # Usamos nuestra TaskView personalizada que tiene el efecto fade y la señal taskSelected
        self.pending_list_view = TaskView(self)
        self.completed_list_view = TaskView(self)

        # --- Configurar el Layout Apilado ---
        self.stacked_layout = QStackedLayout()
        # Añadir las vistas al layout. Guardamos las referencias a los widgets.
        self.stacked_layout.addWidget(self.pending_list_view)
        self.stacked_layout.addWidget(self.completed_list_view)

        # Establecer el layout principal para este widget TaskListManager
        # NOTA: QStackedLayout no se puede establecer directamente con setLayout.
        # Se necesita un layout contenedor o usar QStackedWidget.
        # Solución: Poner el QStackedLayout dentro de un QVBoxLayout simple.
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0,0,0,0) # Sin márgenes extra
        container_layout.addLayout(self.stacked_layout)
        # self.setLayout(container_layout) # No es necesario, QVBoxLayout(self) lo hace

        # --- Conectar Señales Internas ---
        # Conectar la señal 'taskSelected' de AMBAS vistas internas a nuestro slot de retransmisión
        self.pending_list_view.taskSelected.connect(self._relay_task_selected)
        self.completed_list_view.taskSelected.connect(self._relay_task_selected)

        # Establecer la vista inicial (por ejemplo, pendientes)
        self.stacked_layout.setCurrentWidget(self.pending_list_view)

    # --- Slots Públicos ---

    @Slot(int)
    def setCurrentView(self, view_id: int) -> None:
        """
        Cambia la vista de lista visible en el QStackedLayout.

        Args:
            view_id: 1 para la lista de pendientes, 2 para la lista de completadas.
        """
        print(f"TaskListManager: Recibido setCurrentView con ID: {view_id}") # Debug
        if view_id == 1:
            if self.stacked_layout.currentWidget() != self.pending_list_view:
                self.stacked_layout.setCurrentWidget(self.pending_list_view)
                print("TaskListManager: Cambiado a vista Pendientes.") # Debug
        elif view_id == 2:
            if self.stacked_layout.currentWidget() != self.completed_list_view:
                self.stacked_layout.setCurrentWidget(self.completed_list_view)
                print("TaskListManager: Cambiado a vista Completadas.") # Debug
        else:
            print(f"TaskListManager: ID de vista no reconocido: {view_id}") # Debug

    @Slot()
    def refreshModels(self) -> None:
        """
        Llama al método refresh() en los modelos *fuente* asociados a las vistas
        internas (si existen y tienen dicho método).
        """
        print("TaskListManager: Solicitando refresh de modelos fuente...") # Debug
        refreshed_count = 0
        for view in [self.pending_list_view, self.completed_list_view]:
            model = view.model() # Obtener el modelo asignado a la vista (puede ser el proxy)
            source_model = None

            # Verificar si es un proxy model y obtener el fuente
            if isinstance(model, QSortFilterProxyModel):
                source_model = model.sourceModel()
                print(f"TaskListManager: {type(view).__name__} usa ProxyModel. Obteniendo modelo fuente: {type(source_model).__name__}") # Debug
            else:
                source_model = model # No es proxy, usar directamente
                if source_model:
                    print(f"TaskListManager: {type(view).__name__} usa modelo directo: {type(source_model).__name__}") # Debug

            # Verificar si el modelo fuente existe y tiene 'refresh'
            if source_model is not None and hasattr(source_model, 'refresh') and callable(source_model.refresh):
                try:
                    print(f"TaskListManager: Llamando refresh() en modelo fuente de {type(view).__name__}") # Debug
                    source_model.refresh()
                    refreshed_count += 1
                except Exception as e:
                    print(f"TaskListManager: Error al llamar refresh() en el modelo fuente: {e}") # Debug
            elif source_model:
                print(f"TaskListManager: Modelo fuente encontrado pero sin método refresh() para {type(view).__name__}") # Debug
            else:
                print(f"TaskListManager: No se pudo determinar modelo fuente para {type(view).__name__}") # Debug

        print(f"TaskListManager: {refreshed_count} modelos fuente refrescados.") # Debug



    # --- Slots Internos / Privados ---

    @Slot(object) # Recibe el objeto Task (o 'object')
    def _relay_task_selected(self, task) -> None:
        """
        Slot interno que recibe la señal 'taskSelected' de las TaskView
        y la retransmite como 'currentTaskSelected' de este widget.
        """
        if task:
            print(f"TaskListManager: Retransmitiendo selección: {task}") # Debug
            # Emitir nuestra propia señal
            self.currentTaskSelected.emit(task)
        else:
             print(f"TaskListManager: Selección borrada en vista interna.") # Debug


    # --- Métodos de Acceso (Opcional, pero útil) ---

    def getPendingListView(self) -> TaskView:
        """Devuelve la instancia de la vista de lista de pendientes."""
        return self.pending_list_view

    def getCompletedListView(self) -> TaskView:
        """Devuelve la instancia de la vista de lista de completadas."""
        return self.completed_list_view


# --- Ejemplo de Uso Básico ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear ventana principal de prueba
    main_window = QWidget()
    main_window.setWindowTitle("Prueba TaskListManager")
    main_layout = QVBoxLayout(main_window)

    # 1. Crear los botones de cambio de vista
    ListChangeButtons = ListChangeButtons() # Usando dummy o real

    # 2. Crear el gestor de listas
    task_list_manager = TaskListManager()

    # 3. Crear modelos y contenedores (usando dummies aquí)
    pending_container = PendingTasks()
    completed_container = CompletedTasks()
    pending_model = TaskModel(pending_container)
    completed_model = TaskModel(completed_container)

    # Cargar datos de ejemplo
    pending_container.addTask(Task("Pendiente A", "101"))
    completed_container.addTask(Task("Completada X", "201"))
    pending_model.refresh()
    completed_model.refresh()

    # 4. Asignar modelos a las vistas DENTRO del TaskListManager
    task_list_manager.getPendingListView().setModel(pending_model)
    task_list_manager.getCompletedListView().setModel(completed_model)

    # 5. Conectar botones -> gestor (para cambiar vista)
    ListChangeButtons.buttonPressed.connect(task_list_manager.setCurrentView)

    # 6. Conectar gestor -> ventana principal (para saber qué tarea se seleccionó)
    def main_app_handle_selection(selected_task):
        print(f"\n*** Ventana Principal Recibió Selección: {selected_task} ***\n")
    task_list_manager.currentTaskSelected.connect(main_app_handle_selection)

    # Añadir widgets a la ventana principal
    main_layout.addWidget(ListChangeButtons)
    main_layout.addWidget(task_list_manager) # Añadir el gestor

    # Botón para simular refresco
    refresh_button = QPushButton("Refrescar Modelos (Simulado)")
    refresh_button.clicked.connect(task_list_manager.refreshModels)
    main_layout.addWidget(refresh_button)

    main_window.resize(450, 400)
    main_window.show()

    # Simular clic inicial para asegurar estado consistente (opcional)
    ListChangeButtons.buttonPressed.emit(1) # Mostrar pendientes al inicio


    sys.exit(app.exec())

