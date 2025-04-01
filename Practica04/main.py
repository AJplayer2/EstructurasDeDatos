# -*- coding: utf-8 -*-
"""
Archivo principal para la aplicación Gestor de Tareas.

Ensambla la interfaz gráfica y conecta la lógica de negocio.
"""
import sys
import os # Para asegurar rutas de importación

# --- Añadir src al sys.path si main.py está fuera de src ---
# Esto permite importar módulos de src usando src.module
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
# -----------------------------------------------------------

from PySide6.QtCore import Slot, QObject, Qt, QFile, QTextStream
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QMessageBox, QInputDialog, QLineEdit)
from PySide6.QtGui import QCloseEvent
from qt_material import apply_stylesheet

# --- Importar Clases Refactorizadas ---
# Core Logic
try:
    from src.coreClasses.Task import Task
    # Importar CythonQueue renombrada como Queue
    from src.coreClasses.queue_cython import CythonQueue as Queue
    from src.coreClasses.Stack import Stack
    from src.PendingTasks import PendingTasks
    from src.CompletedTasks import CompletedTasks
    from src.FileManager import FileManager
except ImportError as e:
    print(f"Error CRÍTICO importando clases de lógica: {e}. Asegúrate de que 'src' está accesible y las clases existen.")
    sys.exit(1) # Salir si no podemos importar lo básico

# GUI Classes
try:
    from src.GUIClasses.TaskModel import TaskModel # Modelo Adaptador
    from src.GUIClasses.PriorityFilterProxyModel import PriorityFilterProxyModel
    from src.GUIClasses.TaskListView import TaskListView
    from src.GUIClasses.TaskListManager import TaskListManager
    from src.GUIClasses.TaskDetailWidget import TaskDetailWidget
    from src.GUIClasses.ListChangeButtons import ListChangeButtons
    from src.GUIClasses.TaskFilters import TaskFilters
    from src.GUIClasses.TaskManagementButtons import TaskManagementButtons
except ImportError as e:
     print(f"Error CRÍTICO importando clases de GUI: {e}. Asegúrate de que 'src/GUIClasses' existe y las clases están refactorizadas.")
     sys.exit(1)

# --- Clase Principal de la Aplicación ---
class MainWindow(QMainWindow):
    """Ventana principal de la aplicación Gestor de Tareas."""

    def __init__(self, parent: QWidget | None = None):
        """Inicializador de la ventana principal."""
        super().__init__(parent)
        self.setWindowTitle("Gestor de Tareas v1.0")
        self.setGeometry(100, 100, 900, 650) # Posición y tamaño inicial

        # --- Estado de la Aplicación ---
        self._selected_task: Task | None = None # Tarea actualmente seleccionada en la GUI
        self._current_task_id_counter: int = 0 # Último ID numérico utilizado

        # --- Instanciar Componentes Lógicos ---
        # Usar rutas relativas o absolutas según sea necesario
        self.file_manager = FileManager(tasks_filepath="tasks_data.json", id_counter_filepath="task_id_data.json")
        # Cargar datos al inicio
        self._load_data_on_startup()

        # --- Instanciar Modelos Qt ---
        self._setup_models()

        # --- Instanciar Componentes GUI ---
        self._setup_gui_widgets()

        # --- Configurar Layout de la GUI ---
        self._setup_main_layout()

        # --- Conectar Señales y Slots ---
        self._connect_signals()

        # --- Estado Inicial de la GUI ---
        self._update_button_states()
        self.task_detail_view.clear() # Empezar con vista de detalle limpia

        print("Aplicación inicializada correctamente.")

    def _load_data_on_startup(self):
        """Carga el contador de ID y las tareas al iniciar."""
        print("Cargando datos iniciales...")
        self.current_task_id_counter = self.file_manager.load_id_counter()
        self.pending_tasks_container, self.completed_tasks_container = self.file_manager.load_all_data()
        print(f"Carga inicial: {len(self.pending_tasks_container)} pendientes, {len(self.completed_tasks_container)} completadas. Próximo ID: {self.current_task_id_counter + 1}")

    def _setup_models(self):
        """Inicializa los modelos fuente y proxy."""
        print("Configurando modelos Qt...")
        # Modelos Fuente (Adaptadores)
        self.pending_source_model = TaskModel(self.pending_tasks_container)
        self.completed_source_model = TaskModel(self.completed_tasks_container)

        # Proxy Models (para filtrado)
        self.pending_proxy_model = PriorityFilterProxyModel(self)
        self.completed_proxy_model = PriorityFilterProxyModel(self)

        # Conectar Fuente -> Proxy
        self.pending_proxy_model.setSourceModel(self.pending_source_model)
        self.completed_proxy_model.setSourceModel(self.completed_source_model)
        print("Modelos Qt configurados.")

    def _setup_gui_widgets(self):
        """Instancia todos los widgets personalizados de la GUI."""
        print("Creando widgets de la GUI...")
        self.list_change_buttons = ListChangeButtons()
        self.task_filters = TaskFilters()
        self.task_list_manager = TaskListManager() # Contiene las TaskListView
        self.task_detail_view = TaskDetailWidget()
        self.task_management_buttons = TaskManagementButtons()

        # Asignar los *PROXY MODELS* a las vistas dentro del TaskListManager
        self.task_list_manager.getPendingListView().setModel(self.pending_proxy_model)
        self.task_list_manager.getCompletedListView().setModel(self.completed_proxy_model)

        # Refrescar modelos fuente para que los proxies y vistas muestren datos iniciales
        self.pending_source_model.refresh()
        self.completed_source_model.refresh()
        print("Widgets GUI creados y modelos asignados.")

    def _setup_main_layout(self):
        """Define la disposición de los widgets en la ventana principal."""
        print("Configurando layout principal...")
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget) # Layout vertical principal

        # --- Layout Superior (Cambio de Vista + Botones de Acción) ---
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.list_change_buttons)
        top_layout.addStretch(1) # Empujar botones de acción a la derecha
        top_layout.addWidget(self.task_management_buttons)
        main_layout.addLayout(top_layout)

        # --- Layout Medio (Listas + Detalle) ---
        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.task_list_manager, stretch=1) # Lista ocupa más espacio inicial
        middle_layout.addWidget(self.task_detail_view, stretch=1) # Detalle ocupa espacio similar
        main_layout.addLayout(middle_layout, stretch=1) # Darle más espacio vertical a esta sección

        # --- Layout Inferior (Filtros) ---
        main_layout.addWidget(self.task_filters)

        self.setCentralWidget(central_widget)
        print("Layout principal configurado.")

    def _connect_signals(self):
        """Conecta todas las señales y slots de la aplicación."""
        print("Conectando señales y slots...")
        # Cambiar entre vista Pendiente/Completada
        self.list_change_buttons.buttonPressed.connect(self.task_list_manager.setCurrentView)
        self.list_change_buttons.buttonPressed.connect(self._update_button_states) # Actualizar botones al cambiar vista

        # Cambiar filtro de prioridad
        self.task_filters.filterChanged.connect(self.apply_priority_filter)

        # Seleccionar una tarea en la lista activa
        self.task_list_manager.currentTaskSelected.connect(self.update_detail_view)

        # Editar tarea desde la vista de detalle
        self.task_detail_view.descriptionChanged.connect(self.handle_description_change)
        self.task_detail_view.priorityChanged.connect(self.handle_priority_change)

        # Botones de gestión de tareas
        self.task_management_buttons.addTaskClicked.connect(self.add_new_task)
        self.task_management_buttons.deleteTaskClicked.connect(self.delete_selected_task)
        self.task_management_buttons.completeTaskClicked.connect(self.complete_next_task)
        self.task_management_buttons.saveTasksClicked.connect(self.save_all_tasks)
        self.task_management_buttons.loadTasksClicked.connect(self.load_all_tasks)
        print("Señales y slots conectados.")

    # --- Slots de Lógica de Aplicación ---

    @Slot(int)
    def apply_priority_filter(self, priority_id: int):
        """Aplica el filtro de prioridad a ambos proxy models."""
        print(f"Aplicando filtro de prioridad ID: {priority_id}")
        self.pending_proxy_model.setPriorityFilter(priority_id)
        self.completed_proxy_model.setPriorityFilter(priority_id)

    @Slot(object) # Recibe Task o None
    def update_detail_view(self, task: Task | None):
        """Actualiza la vista de detalles y el estado interno con la tarea seleccionada."""
        print(f"Actualizando vista de detalle para: {task}")
        self._selected_task = task # Guardar referencia a la tarea seleccionada (o None)
        self.task_detail_view.setTaskData(task) # setTaskData maneja None internamente
        self._update_button_states() # Actualizar habilitación de botones

    @Slot(int, str)
    def handle_description_change(self, task_id: int, new_description: str):
        """Maneja la edición de la descripción desde la vista de detalles."""
        print(f"Intentando actualizar descripción para Task ID: {task_id}")
        # Buscar en qué contenedor está la tarea y editarla
        if self.pending_tasks_container.editTask(task_id, "description", new_description):
            print("Descripción actualizada en Pendientes.")
            self.pending_source_model.refresh() # Refrescar modelo (y vista proxy)
        elif self.completed_tasks_container.editTask(task_id, "description", new_description):
            print("Descripción actualizada en Completadas.")
            self.completed_source_model.refresh() # Refrescar modelo (y vista proxy)
        else:
            print(f"Error: No se encontró la tarea con ID {task_id} para editar descripción.")
            QMessageBox.warning(self, "Error", f"No se pudo encontrar la tarea (ID: {task_id}) para editar.")
        # No es necesario actualizar la vista de detalle aquí, ya refleja el cambio local

    @Slot(int, int)
    def handle_priority_change(self, task_id: int, new_priority_id: int):
        """Maneja la edición de la prioridad desde la vista de detalles."""
        print(f"Intentando actualizar prioridad para Task ID: {task_id} a {new_priority_id}")
        task_refreshed = False
        # Buscar y editar en el contenedor apropiado
        if self.pending_tasks_container.editTask(task_id, "priority", new_priority_id):
            print("Prioridad actualizada en Pendientes.")
            self.pending_source_model.refresh()
            task_refreshed = True
        elif self.completed_tasks_container.editTask(task_id, "priority", new_priority_id):
            print("Prioridad actualizada en Completadas.")
            self.completed_source_model.refresh()
            task_refreshed = True
        else:
             print(f"Error: No se encontró la tarea con ID {task_id} para editar prioridad.")
             QMessageBox.warning(self, "Error", f"No se pudo encontrar la tarea (ID: {task_id}) para editar.")

        # Si la tarea editada era la seleccionada, actualizar su formato en la vista de detalle
        if task_refreshed and self._selected_task and self._selected_task.task_id == task_id:
             # Volver a cargar los datos en la vista de detalle para reflejar el cambio de prioridad visualmente
             # (Aunque el combobox ya cambió, el texto en la lista no lo haría sin refresh)
             # Es más simple confiar en que el refresh del modelo actualizará la lista,
             # y si la tarea sigue seleccionada, update_detail_view se llamará de nuevo.
             # O podemos forzar la actualización aquí:
             # self.update_detail_view(self._selected_task) # Cuidado con bucles si la señal se emite de nuevo
             pass # Dejar que el refresh del modelo maneje la actualización visual de la lista


    @Slot()
    def add_new_task(self):
        """Abre diálogos para añadir una nueva tarea pendiente."""
        print("Iniciando proceso para añadir nueva tarea...")
        # 1. Obtener Título
        title, ok1 = QInputDialog.getText(self, "Añadir Tarea", "Título:", QLineEdit.EchoMode.Normal)
        if not ok1 or not title.strip():
            print("Cancelado o título vacío.")
            return # Cancelado o vacío

        # 2. Obtener Descripción
        description, ok2 = QInputDialog.getMultiLineText(self, "Añadir Tarea", "Descripción:", "")
        if not ok2:
            print("Cancelado.")
            return # Cancelado

        # 3. Obtener Prioridad
        priorities = {name: id_ for name, id_ in TaskDetailWidget.PRIORITY_MAP_STR_TO_INT.items()}
        priority_name, ok3 = QInputDialog.getItem(self, "Añadir Tarea", "Prioridad:",
                                                  list(priorities.keys()), 0, False) # Editable=False
        if not ok3:
            print("Cancelado.")
            return # Cancelado
        priority_id = priorities[priority_name]

        # 4. Crear y añadir la tarea
        try:
            self.current_task_id_counter += 1 # Incrementar ANTES de crear
            new_task = Task(
                task_id=self.current_task_id_counter,
                title=title.strip(),
                description=description, # Mantener saltos de línea
                status=Task.STATUS_PENDING, # Siempre pendiente al añadir
                priority=priority_id
            )
            print(f"Tipo de la tarea: {type(new_task)}")
            self.pending_tasks_container.addTask(new_task)
            self.pending_source_model.refresh() # Actualizar modelo/vista
            print(f"Nueva tarea añadida: {new_task}")
            # Seleccionar la nueva tarea añadida en la vista
            self.task_list_manager.getPendingListView().selectTaskById(new_task.task_id)
        except Exception as e:
            print(f"Error al crear o añadir la nueva tarea: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo añadir la tarea:\n{e}")
            # Revertir contador si la creación falló después de incrementar? Podría ser complejo.
            # Es más simple aceptar que puede haber saltos de ID si hay errores.

        self._update_button_states()

    @Slot()
    def delete_selected_task(self):
        """Elimina la tarea pendiente actualmente seleccionada."""
        if self._selected_task and self._selected_task.status == Task.STATUS_PENDING:
            confirm = QMessageBox.question(self, "Confirmar Eliminación",
                                           f"¿Seguro que quieres eliminar la tarea pendiente:\n'{self._selected_task.title}'?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                           QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                print(f"Eliminando tarea ID: {self._selected_task.task_id}")
                if self.pending_tasks_container.removeTask(self._selected_task):
                    print("Tarea eliminada del contenedor.")
                    self.pending_source_model.refresh()
                    self._selected_task = None # Limpiar selección interna
                    self.task_detail_view.clear() # Limpiar vista detalle
                    self._update_button_states()
                    QMessageBox.information(self, "Éxito", "Tarea eliminada correctamente.")
                else:
                    print("Error: La tarea seleccionada no se pudo eliminar del contenedor.")
                    QMessageBox.warning(self, "Error", "No se pudo eliminar la tarea seleccionada.")
        else:
            print("No hay tarea pendiente seleccionada para eliminar.")
            QMessageBox.information(self, "Eliminar Tarea", "Selecciona una tarea pendiente para eliminar.")

    @Slot()
    def complete_next_task(self):
        """Marca la siguiente tarea pendiente (FIFO) como completada."""
        print("Intentando completar la siguiente tarea pendiente...")
        completed_task = self.pending_tasks_container.completeTask() # Saca de pendientes y cambia estado
        if completed_task:
            print(f"Tarea completada: {completed_task}")
            self.completed_tasks_container.addTask(completed_task) # Añade a completadas
            # Refrescar ambos modelos
            self.pending_source_model.refresh()
            self.completed_source_model.refresh()
            self._update_button_states()
            # Opcional: Mostrar un mensaje
            # QMessageBox.information(self, "Tarea Completada", f"Se completó la tarea:\n'{completed_task.title}'")
            # Opcional: Seleccionar la tarea recién completada en la vista de completadas
            # self.list_change_buttons.completed_button.click() # Cambiar a vista completadas
            # self.task_list_manager.getCompletedListView().selectTaskById(completed_task.task_id)
        else:
            print("No hay tareas pendientes para completar.")
            QMessageBox.information(self, "Completar Tarea", "No hay tareas pendientes para completar.")

    @Slot()
    def save_all_tasks(self):
        """Guarda el estado actual de las tareas y el contador de ID."""
        print("Guardando todas las tareas y contador...")
        # Guardar tareas
        tasks_saved = self.file_manager.save_all_data(self.pending_tasks_container, self.completed_tasks_container)
        # Guardar contador
        counter_saved = self.file_manager.save_id_counter(self.current_task_id_counter)

        if tasks_saved and counter_saved:
            print("Datos guardados exitosamente.")
            QMessageBox.information(self, "Guardado", "Tareas y estado guardados correctamente.")
        else:
            error_msg = []
            if not tasks_saved: error_msg.append("Error al guardar las tareas.")
            if not counter_saved: error_msg.append("Error al guardar el contador de ID.")
            print("Error durante el guardado.")
            QMessageBox.critical(self, "Error al Guardar", "\n".join(error_msg))

    @Slot()
    def load_all_tasks(self):
        """Carga las tareas desde el archivo, reemplazando el estado actual."""
        confirm = QMessageBox.question(self, "Confirmar Carga",
                                       "¿Seguro que quieres cargar las tareas desde el archivo?\n"
                                       "Se perderán los cambios no guardados.",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            print("Cargando tareas desde archivo...")
            try:
                # Cargar contenedores
                pending_loaded, completed_loaded = self.file_manager.load_all_data()
                self.pending_tasks_container = pending_loaded
                self.completed_tasks_container = completed_loaded

                # Cargar contador
                self.current_task_id_counter = self.file_manager.load_id_counter()

                # Actualizar modelos con los nuevos contenedores
                self.pending_source_model.set_task_container(self.pending_tasks_container)
                self.completed_source_model.set_task_container(self.completed_tasks_container)

                # Refrescar modelos/vistas
                self.pending_source_model.refresh()
                self.completed_source_model.refresh()

                # Limpiar estado de la GUI
                self._selected_task = None
                self.task_detail_view.clear()
                self._update_button_states()

                print("Carga completada.")
                QMessageBox.information(self, "Carga Completa", "Tareas cargadas correctamente desde el archivo.")

            except Exception as e:
                print(f"Error durante la carga: {e}")
                QMessageBox.critical(self, "Error al Cargar", f"Ocurrió un error al cargar los datos:\n{e}")

    @Slot()
    def _update_button_states(self):
        """Actualiza el estado habilitado/deshabilitado de los botones de gestión."""
        # print("Actualizando estado de botones...") # Debug frecuente
        is_pending_selected = (self._selected_task is not None and
                               self._selected_task.status == Task.STATUS_PENDING)
        is_any_task_selected = (self._selected_task is not None)
        # El botón Complete depende de si hay algo en la cola, no de la selección
        can_complete = not self.pending_tasks_container.tasks.isEmpty()

        self.task_management_buttons.enableCompleteButton(can_complete)
        self.task_management_buttons.enableDeleteButton(is_pending_selected)
        # Add, Save, Load suelen estar siempre habilitados
        self.task_management_buttons.enableAddButton(True)

    # --- Manejo de Cierre de Aplicación ---
    def closeEvent(self, event: QCloseEvent):
        """Se ejecuta al intentar cerrar la ventana."""
        print("Evento de cierre detectado.")
        reply = QMessageBox.question(self, 'Confirmar Salida',
                                     "¿Guardar cambios antes de salir?",
                                     QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                                     QMessageBox.StandardButton.Cancel) # Default a Cancelar

        if reply == QMessageBox.StandardButton.Save:
            self.save_all_tasks()
            event.accept() # Aceptar cierre
        elif reply == QMessageBox.StandardButton.Discard:
            event.accept() # Aceptar cierre sin guardar
        else:
            event.ignore() # Ignorar el evento de cierre, no cerrar


# --- Bloque Principal de Ejecución ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- Cargar y Aplicar Estilo ---
    apply_stylesheet(app, "dark_blue.xml",)

    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()

    # Ejecutar el bucle de eventos de la aplicación
    sys.exit(app.exec())