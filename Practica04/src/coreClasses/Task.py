class Task:
    id_counter = 1

    #Cada tarea tiene un ID distinto, sirve para facilitar la busqueda de tareas, el primer digito del ID representa su urgencia
    def __init__(self, priority:int, title:str, description:str, status:str):
        #la prioridad va de 3 a 1, urgente, media y baja respectivamente.
        self.priority = priority
        self.title = title
        self.description = description
        self.status = status
        self.ID = str(priority)+str(self.id_counter)
        Task.id_counter += 1

    def changeStatus(self, newStatus:str):
        self.status = newStatus

    def editTitle(self, newTitle:str):
        self.title = newTitle

    def editDescription(self, newDescription=str):
        self.description = newDescription

    def editPriority(self, newPriority:int):
        self.priority = newPriority 
        self.ID = str(newPriority)+str(self.ID[1:])