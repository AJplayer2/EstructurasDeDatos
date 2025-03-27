import tkinter as tk
import ttkbootstrap as ttk
from src import CompletedTasks, PendingTasks
import src.coreClasses.Task as Task
import src.FileManager as FileManager

if __name__ == "__main__":
        
    
    filepath = './Tasks.txt'
    
    tareasCompletadas = FileManager.readCompleted(filepath)
    tareasPendientes = FileManager.readPending(filepath)
    for i in range(0,5):
        tareasPendientes.addTask(Task.Task.taskCreate(3,'title','description','status'))

    tareasCompletadas.addTask(tareasPendientes.completeTask())    

    listaTareas = tareasPendientes.taskList()

    FileManager.saveTasks(filepath, tareasCompletadas, tareasPendientes)    


    # for item in listaTareas:
    #     print(f'{getattr(item, "title")} {getattr(item, 'description')} {getattr(item, 'ID')}')