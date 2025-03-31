# -*- coding: utf-8 -*-
import sys
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Slot, QObject
from PySide6.QtWidgets import QApplication, QListView, QVBoxLayout, QWidget, QPushButton, QLabel # Para el ejemplo

# --- Importación de Clases de Tareas y Contenedores ---
# Intenta importar las clases reales. Ajusta las rutas si es necesario.
try:
    from src.coreClasses.Task import Task
    # Asumimos que PendingTasks y CompletedTasks están en 'src'
    # y tienen un método 'taskList()' que devuelve una lista de Tasks
    from src.PendingTasks import PendingTasks
    from src.CompletedTasks import CompletedTasks
except ImportError as e:
    # Definiciones de ejemplo si las importaciones fallan
    print(f"ADVERTENCIA: Falló la importación ({e}). Usando clases de ejemplo.")
    class Task:
        def __init__(self, title="Dummy Task", description="...", status="Pendiente", ID="10"):
            self.title = title
            self.description = description
            self.status = status
            self.ID = ID
            try:
                self.priority = int(ID[0]) if ID else 1
            except ValueError: self.priority = 1
        def __repr__(self): return f"Task(ID='{self.ID}', Title='{self.title}')"

    class PendingTasks: # Clase de ejemplo
        def __init__(self): self.items = []
        def taskList(self): return sorted(self.items, key=lambda x: x.priority, reverse=True)
        def addTask(self, task): self.items.append(task) # Solo para prueba

    class CompletedTasks: # Clase de ejemplo
        def __init__(self): self.items = []
        def taskList(self): return list(self.items)
        def addTask(self, task): self.items.append(task) # Solo para prueba

# --- Implementación del Modelo TaskModel como Adaptador ---
class TaskModel(QAbstractListModel):
    """
    Modelo Qt que actúa como adaptador para un contenedor de tareas
    (como PendingTasks o CompletedTasks).

    Este modelo no almacena las tareas directamente, sino que lee la lista
    del contenedor asociado a través de su método 'taskList()'.
    Utiliza una caché interna para eficiencia y notifica a las vistas
    cuando los datos necesitan ser refrescados usando 'refresh()'.
    """

    # Rol para obtener el objeto Task completo desde el modelo/caché
    TaskObjectRole = Qt.ItemDataRole.UserRole + 1

    def __init__(self, task_container: object | None = None, parent: QObject | None = None):
        """
        Inicializador del modelo.

        Args:
            task_container: La instancia de PendingTasks o CompletedTasks
                            que este modelo representará.
            parent: El objeto padre Qt (opcional).
        """
        super().__init__(parent)
        self._task_container = task_container
        # Caché interna para la lista de tareas obtenida del contenedor.
        # rowCount() y data() usarán esta caché.
        self._tasks_cache: list[Task] = []
        # Realizar una actualización inicial si ya tenemos un contenedor
        # Es mejor llamar a refresh() explícitamente desde fuera después de crear.

    def set_task_container(self, container: object) -> None:
        """Asigna o cambia el contenedor de tareas (PendingTasks/CompletedTasks)."""
        print(f"TaskModel: Estableciendo contenedor: {type(container)}")
        self._task_container = container
        # Es importante llamar a refresh() después de asignar un contenedor
        # para cargar los datos iniciales en la caché y la vista.
        # self.refresh() # O llamar desde fuera

    @Slot()
    def refresh(self) -> None:
        """
        Actualiza la caché interna del modelo leyendo desde el contenedor
        de tareas asociado y notifica a las vistas para que se actualicen.

        Este método debe ser llamado externamente cuando los datos en el
        contenedor (PendingTasks/CompletedTasks) han cambiado.
        """
        print(f"TaskModel: Iniciando refresh desde {type(self._task_container).__name__}")
        tasks = []
        if self._task_container and hasattr(self._task_container, 'taskList') and callable(self._task_container.taskList):
            try:
                # Obtener la lista actualizada de tareas desde el contenedor
                tasks = self._task_container.taskList()
                if tasks is None: # Asegurarse de que taskList no devuelva None
                    tasks = []
                print(f"TaskModel: Contenedor devolvió {len(tasks)} tareas.")
            except Exception as e:
                print(f"TaskModel: Error al llamar a taskList() del contenedor: {e}")
                tasks = [] # Dejar la caché vacía en caso de error
        else:
            print(f"TaskModel: Contenedor no válido o sin método taskList().")

        # Notificar a las vistas que el modelo se reseteará completamente
        # (necesario porque no sabemos qué cambió exactamente: añadidos, eliminados, reordenados?)
        self.beginResetModel()
        # Actualizar la caché interna con la lista obtenida
        self._tasks_cache = list(tasks) # Guardar como lista
        # Notificar a las vistas que el reseteo ha terminado
        self.endResetModel()
        print(f"TaskModel: Refresh completo. Tamaño de caché: {len(self._tasks_cache)}")

    # --- Métodos Obligatorios (usan la caché interna) ---

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Devuelve el número de filas basado en la caché interna."""
        return len(self._tasks_cache) if not parent.isValid() else 0

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> object | None:
        """Devuelve los datos para un índice y rol específicos desde la caché."""
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return None

        # Obtener la tarea desde la caché interna
        try:
            task = self._tasks_cache[index.row()]
        except IndexError:
             print(f"TaskModel: Error de índice en data() - Fila: {index.row()}, Tamaño caché: {len(self._tasks_cache)}")
             return None

        # Rol para mostrar texto
        if role == Qt.ItemDataRole.DisplayRole:
            prio_map = {3: "Urgente", 2: "Medio", 1: "Bajo"}
            prio_text = prio_map.get(getattr(task, 'priority', 0), "N/A") # Usar getattr por si acaso
            title_text = getattr(task, 'title', 'Sin Título')
            return f"{title_text} ({prio_text})"

        # Rol para obtener el objeto Task completo
        if role == Qt.ItemDataRole.UserRole:
            return task

        return None

    # --- Método Auxiliar (opera sobre la caché) ---
    def getTaskFromRow(self, row: int) -> Task | None:
        """Obtiene el objeto Task en la fila especificada (desde la caché)."""
        if 0 <= row < self.rowCount():
             try:
                return self._tasks_cache[row]
             except IndexError:
                 print(f"TaskModel: Error de índice en getTaskFromRow() - Fila: {row}, Tamaño caché: {len(self._tasks_cache)}")
                 return None
        return None


# --- Ejemplo de Uso Básico (si ejecutas este archivo directamente) ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear contenedores de tareas (instancias reales o de ejemplo)
    pending_tasks_container = PendingTasks()
    completed_tasks_container = CompletedTasks()

    # Añadir algunas tareas de ejemplo directamente a los contenedores
    pending_tasks_container.addTask(Task(title="Tarea Pendiente 1", ID="301"))
    pending_tasks_container.addTask(Task(title="Tarea Pendiente 2", ID="102"))
    completed_tasks_container.addTask(Task(title="Tarea Completada 1", ID="203", status="Completed"))

    # Crear instancias del modelo, una para cada contenedor
    pending_model = TaskModel(pending_tasks_container)
    completed_model = TaskModel(completed_tasks_container)

    # --- IMPORTANTE: Llamar a refresh() después de crear/asignar contenedor ---
    pending_model.refresh()
    completed_model.refresh()

    # Crear vistas y asignar modelos
    pending_view = QListView()
    pending_view.setModel(pending_model)
    completed_view = QListView()
    completed_view.setModel(completed_model)

    # --- Simulación de cambios externos y actualización del modelo ---
    def complete_first_pending():
        print("\n--- Simulando completar tarea ---")
        if pending_tasks_container.items:
            # 1. Modificar los contenedores reales
            task_to_complete = pending_tasks_container.items.pop(0) # Simula dequeue/remove
            task_to_complete.status = "Completed"
            completed_tasks_container.addTask(task_to_complete)
            print(f"Tarea '{task_to_complete.title}' movida a completadas.")

            # 2. Notificar a AMBOS modelos que deben refrescarse
            print("Refrescando modelo de pendientes...")
            pending_model.refresh()
            print("Refrescando modelo de completadas...")
            completed_model.refresh()
        else:
            print("No hay tareas pendientes para completar.")

    # Crear ventana de prueba
    window = QWidget()
    window.setWindowTitle("Prueba TaskModel Adaptador")
    layout = QVBoxLayout(window)
    layout.addWidget(QLabel("Tareas Pendientes:"))
    layout.addWidget(pending_view)
    layout.addWidget(QLabel("Tareas Completadas:"))
    layout.addWidget(completed_view)

    button_complete = QPushButton("Completar Primera Tarea Pendiente")
    button_complete.clicked.connect(complete_first_pending)
    layout.addWidget(button_complete)

    window.resize(400, 500)
    window.show()
    sys.exit(app.exec())

