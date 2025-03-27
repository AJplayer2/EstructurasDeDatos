import tkinter as tk
import ttkbootstrap as ttk
from src import CompletedTasks, PendingTasks
import src.coreClasses.Task as Task

if __name__ == "__main__":
    task = Task.Task(1, "NuevaTarea", "Descripcion","Pendiente")
    task1 = Task.Task(2, "NuevaTarea", "Descripcion","Pendiente")
    task2 = Task.Task(1, "NuevaTarea", "Descripcion","Pendiente")
    task3 = Task.Task(3, "NuevaTarea", "Descripcion","Pendiente")
    tareasPendientes = PendingTasks.PendingTasks()
    tareasPendientes.addTask(task)
    tareasPendientes.addTask(task1)
    tareasPendientes.addTask(task2)
    tareasPendientes.addTask(task3)    
    listaTareas = tareasPendientes.taskList()
    for item in listaTareas:
        print(getattr(item, "title")+" "+getattr(item, "description")+" "+getattr(item, "ID"))