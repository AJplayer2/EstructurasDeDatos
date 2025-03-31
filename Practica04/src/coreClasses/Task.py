import os, json
class Task:
    #Contador para los ID distintos y el archivo para no perder el cambio en el contador
    _id_file = "task_id.json"
    _id_counter = 1

    #Carga el archivo con el contador o lo crea de no existir
    @classmethod
    def _load_last_id(self):
        """Load last used ID from file."""
        if os.path.exists(self._id_file):
            with open(self._id_file, "r") as f:
                self._id_counter = json.load(f) + 1
        else:
            self._id_counter = 1

    #Guarda el archivo con el contador
    @classmethod
    def _save_last_id(self):
        """Save the current ID to file."""
        with open(self._id_file, "w") as f:
            json.dump(self._id_counter, f)

    @classmethod
    def taskCreate(self, priority:int, title:str, description:str, status:str):
        #la prioridad va de 3 a 1, urgente, media y baja respectivamente.
        self._load_last_id()
        newID = str(priority)+str(self._id_counter)
        self._save_last_id()
        return self(title, description, status, newID)
        

    def __init__(self, title:str, description:str, status:str, ID:str):
        self.title = title
        self.description = description
        self.status = status
        self.ID = ID
        self.priority = int(ID[0])

    #Cada tarea tiene un ID distinto, sirve para facilitar la busqueda de tareas, el primer digito del ID representa su urgencia


    def changeStatus(self, newStatus:str):
        self.status = newStatus

    def editTitle(self, newTitle:str):
        self.title = newTitle

    def editDescription(self, newDescription:str=""):
        self.description = newDescription

    def editPriority(self, newPriority:int):
        self.priority = newPriority 
        self.ID = str(newPriority)+str(self.ID[1:])

    def write(self):
        return f"{self.title}|{self.description}|{self.status}|{self.ID}"