import src.coreClasses.Task as task
import src.coreClasses.Queue as Queue

#Clase para las tareas pendientes
class PendingTasks:
    def __init__(self):
        self.tasks = Queue.Queue()

    def addTask(self, item:task):
        self.tasks.enqueue(item)
    
    def completeTask(self):
        completedTask:task = self.tasks.dequeue()
        completedTask.changeStatus("Completed")
        return completedTask

    def removeTask(self, item:task):
        self.tasks.removeTask(item)

    def editTask(self, item:task, attribute, newValue):
        for t in self.tasks.items:
            if getattr(t, "ID") == getattr(item, "ID"):
                match attribute:
                    case "title":
                        t.editTitle(newValue)
                    case "description":
                        t.editDescription(newValue)
                    case "priority":
                        t.editPriority(newValue)
    #Usado para visualizar las tareas pendientes, ordena las tareas segun su prioridad de urgente a baja.
    def taskList(self):
        return sorted(self.tasks.items, key=lambda x: getattr(x,"priority"), reverse=True)