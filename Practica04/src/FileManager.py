# -*- coding: utf-8 -*-
"""
Módulo para gestionar la persistencia de datos (tareas y contador de IDs)
usando archivos JSON.
"""
import os
import json # Importar el módulo JSON
from typing import Tuple # Para type hinting de la tupla de retorno

from src.coreClasses.Task import Task
from src.PendingTasks import PendingTasks
from src.CompletedTasks import CompletedTasks
class FileManager:
    """
    Gestiona la carga y guardado de tareas y del contador de IDs
    usando archivos JSON.
    """
    DEFAULT_TASKS_FILENAME = "tasks_data.json"
    DEFAULT_ID_FILENAME = "task_id_counter.json"

    def __init__(self, tasks_filepath: str = DEFAULT_TASKS_FILENAME, id_counter_filepath: str = DEFAULT_ID_FILENAME):
        """
        Inicializa el FileManager con las rutas a los archivos.
        """
        if not isinstance(tasks_filepath, str) or not tasks_filepath:
            raise ValueError("tasks_filepath debe ser una cadena no vacía.")
        if not isinstance(id_counter_filepath, str) or not id_counter_filepath:
            raise ValueError("id_counter_filepath debe ser una cadena no vacía.")

        self.tasks_filepath = tasks_filepath
        self.id_counter_filepath = id_counter_filepath
        print(f"FileManager (JSON) inicializado. Archivo tareas: '{self.tasks_filepath}', Archivo contador: '{self.id_counter_filepath}'")

    # --- Gestión del Contador de IDs ---

    def load_id_counter(self) -> int:
        """Carga el último ID de tarea utilizado desde el archivo JSON."""
        print(f"FileManager: Intentando cargar contador desde '{self.id_counter_filepath}'")
        if not os.path.exists(self.id_counter_filepath):
            print("FileManager: Archivo de contador no encontrado, empezando desde 0.")
            return 0
        try:
            with open(self.id_counter_filepath, 'r', encoding='utf-8') as f:
                last_id = json.load(f)
                if isinstance(last_id, int) and last_id >= 0:
                    print(f"FileManager: Último ID cargado: {last_id}")
                    return last_id
                else:
                    print(f"Error: Contenido inválido en '{self.id_counter_filepath}'. Empezando desde 0.")
                    return 0
        except (IOError, json.JSONDecodeError, ValueError) as e:
            print(f"Error al cargar el contador de ID desde '{self.id_counter_filepath}': {e}. Empezando desde 0.")
            return 0

    def save_id_counter(self, last_id: int) -> bool:
        """Guarda el último ID de tarea utilizado en el archivo JSON."""
        print(f"FileManager: Intentando guardar último ID ({last_id}) en '{self.id_counter_filepath}'")
        if not isinstance(last_id, int) or last_id < 0:
             print(f"Error: Se intentó guardar un ID inválido ({last_id}).")
             return False
        try:
            os.makedirs(os.path.dirname(self.id_counter_filepath) or '.', exist_ok=True)
            with open(self.id_counter_filepath, 'w', encoding='utf-8') as f:
                # Guardar como JSON simple
                json.dump(last_id, f)
            print("FileManager: Contador de ID guardado correctamente.")
            return True
        except (IOError, TypeError) as e:
            print(f"Error al guardar el contador de ID en '{self.id_counter_filepath}': {e}")
            return False

    # --- Gestión de Tareas (Usando JSON) ---s

    def load_all_data(self) -> Tuple[PendingTasks, CompletedTasks]:
        """
        Carga las tareas pendientes y completadas desde el archivo JSON.

        Returns:
            Una tupla conteniendo (PendingTasks, CompletedTasks) pobladas.
            Si el archivo no existe o está vacío/corrupto, devuelve contenedores vacíos.
        """
        print(f"FileManager: Intentando cargar tareas desde '{self.tasks_filepath}' (JSON)")
        pending_tasks = PendingTasks()
        completed_tasks = CompletedTasks()

        if not os.path.exists(self.tasks_filepath):
            print("FileManager: Archivo de tareas JSON no encontrado. Devolviendo contenedores vacíos.")
            return pending_tasks, completed_tasks

        try:
            with open(self.tasks_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f) # Cargar toda la estructura JSON

            # Procesar tareas completadas
            completed_data = data.get("completed_tasks", []) # Usar .get con default lista vacía
            print(f"FileManager: Cargando {len(completed_data)} tareas completadas...")
            for task_dict in completed_data:
                try:
                    # Usar el método de clase Task.from_dict (necesita existir en Task)
                    task = Task.from_dict(task_dict)
                    completed_tasks.addTask(task)
                except (ValueError, KeyError, TypeError) as e:
                    print(f"Advertencia: Error al procesar diccionario de tarea completada: {e} -> {task_dict}. Tarea ignorada.")

            # Procesar tareas pendientes
            pending_data = data.get("pending_tasks", [])
            print(f"FileManager: Cargando {len(pending_data)} tareas pendientes...")
            for task_dict in pending_data:
                 try:
                    task = Task.from_dict(task_dict)
                    pending_tasks.addTask(task)
                 except (ValueError, KeyError, TypeError) as e:
                    print(f"Advertencia: Error al procesar diccionario de tarea pendiente: {e} -> {task_dict}. Tarea ignorada.")

        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al leer o parsear el archivo JSON de tareas '{self.tasks_filepath}': {e}")
            # Devolver contenedores vacíos en caso de error grave de lectura/parseo
            return PendingTasks(), CompletedTasks()
        except Exception as e: # Captura genérica para otros errores inesperados
             print(f"Error inesperado durante la carga de tareas desde JSON: {e}")
             return PendingTasks(), CompletedTasks()


        print(f"FileManager: Carga JSON completada. {len(pending_tasks)} pendientes, {len(completed_tasks)} completadas.")
        return pending_tasks, completed_tasks

    def save_all_data(self, pending_tasks: PendingTasks, completed_tasks: CompletedTasks) -> bool:
        """
        Guarda las tareas pendientes y completadas en el archivo JSON,
        sobrescribiendo el contenido anterior.

        Args:
            pending_tasks: El contenedor de tareas pendientes.
            completed_tasks: El contenedor de tareas completadas.

        Returns:
            True si se guardó correctamente, False en caso contrario.
        """
        print(f"FileManager: Intentando guardar tareas en '{self.tasks_filepath}' (JSON)")
        try:
            # Crear listas de diccionarios usando el método to_dict de Task
            # Iterar sobre los contenedores para obtener las tareas en su orden interno
            pending_list = [task.to_dict() for task in pending_tasks.taskList()]
            completed_list = [task.to_dict() for task in completed_tasks.taskList()]

            # Crear la estructura de datos a guardar
            data_to_save = {
                "pending_tasks": pending_list,
                "completed_tasks": completed_list
            }

            # Crear directorios si no existen
            os.makedirs(os.path.dirname(self.tasks_filepath) or '.', exist_ok=True)

            # Escribir el archivo JSON
            with open(self.tasks_filepath, 'w', encoding='utf-8') as f:
                # Usar indent=4 para que el archivo JSON sea legible por humanos
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)

            print(f"FileManager: Tareas guardadas correctamente en '{self.tasks_filepath}' (JSON).")
            return True
        except (IOError, AttributeError, TypeError) as e:
            # AttributeError/TypeError si los contenedores o tareas no tienen los métodos/atributos esperados (ej. __iter__, to_dict)
            print(f"Error al guardar el archivo JSON de tareas '{self.tasks_filepath}': {e}")
            return False
        except Exception as e: # Captura genérica
             print(f"Error inesperado durante el guardado JSON: {e}")
             return False