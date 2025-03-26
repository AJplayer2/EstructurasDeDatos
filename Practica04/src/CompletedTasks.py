import src.coreClasses.Task as task
import src.coreClasses.Stack as stack

#Clase para las tareas completadas
class CompletedTasks:
    def __init__(self):
        self.tasks = stack()
    
    def addTask(self, item:task):
        self.tasks.append(item)

    def getTasks(self):
        return self.tasks
    
    def editTask(self, item:task, attribute, newValue):
        for t in self.tasks:
            if getattr(t, "ID") == getattr(item, "ID"):
                match attribute:
                    case "title":
                        t.editTitle(newValue)
                    case "description":
                        t.editDescription(newValue)
                    case "priority":
                        t.editPriority(newValue)

    def taskList(self):
        return list(self.tasks)