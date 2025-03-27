import coreClasses.Task as tsk
import CompletedTasks as CT
import PendingTasks as PT
import os

def saveTasks(filePath, ctasks:CT.CompletedTasks, ptasks:PT.PendingTasks):
    with open(filePath, 'w') as f:
        f.write("Completed Tasks:\n")
        for task in ctasks.tasks.items:
            f.write(f'{task}\n')
        f.write('\nPendingTasks:\n')
        for task in ptasks.tasks.items:
            f.write(f'{task}\n')
    return 'Tasks succesfully saved!'

def readPending(filePath):
    pending_tasks = PT.PendingTasks()

    if not os.path.exists(filePath):
        return pending_tasks

    with open(filePath, "r") as f:
        lines = f.readlines()
    
    reading_pending = False

    for line in lines:
        line = line.strip()
        if line == "Pending Tasks:":
            reading_pending = True
            continue
        elif reading_pending and line:
            parts = line.split("|")
            title, description, status, task_id = parts
            pending_tasks.addTask(tsk.Task(title, description, status, task_id))

    return pending_tasks

def readCompleted(filePath):
    ctasks = PT.PendingTasks()
    
    if not os.path.exists(filePath):
        return ctasks
    
    with open(filePath, 'r') as f:
        lines = f.readlines()
    
    reading_completed = False 

    for line in lines:
        line = line.strip()
        if line == "Completed Tasks:":
            reading_completed = True
            continue
        elif line == "Pending Tasks:":
            break
        elif reading_completed and line:
            parts = line.split("|")
            title, description, status, task_id = parts
            ctasks.addTask(tsk.Task(title, description, status, task_id))

    return ctasks
