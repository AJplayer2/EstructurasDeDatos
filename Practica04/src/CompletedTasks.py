import coreClasses.Task as task
import coreClasses.Stack as Stack

#Clase para las tareas completadas
class CompletedTasks:
    def __init__(self):
        self.tasks = Stack.Stack()
    
    def addTask(self, item:task):
        self.tasks.append(item)

    def getTasks(self):
        return self.tasks
    
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

    def taskList(self):
        return list(self.tasks.items)