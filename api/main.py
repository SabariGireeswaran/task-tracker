from fastapi import FastAPI
from pydantic import BaseModel

from core.manager import TaskManager
from storage.json_store import JsonTaskStore

app = FastAPI(title = "Task Tracker API")

# ---- Dependency setup (same as CLI) ---- 
store = JsonTaskStore("tasks.json")
manager = TaskManager(store)

# ---- Request schema FIRST ----
class TaskCreate(BaseModel):

    description: str

class TaskResponse(BaseModel):
    id: int
    description: str
    status: str
    createdAt: str
    updatedAt: str

class MessageResponse(BaseModel):
    message: str

# ---- Routes AFTER ----
@app.get("/", response_model = MessageResponse)
def root():
    return {"message": "Task Tracker API is running"}

@app.post("/tasks", response_model = TaskResponse)
def create_task(task: TaskCreate):
    new_task = manager.add_task(task.description)
    return new_task.to_dict()

@app.get("/tasks")
def list_tasks(status: str | None = None):
    tasks = manager.list_tasks(status)
    
    if not tasks:
        return {"message": "No tasks found"}
    
    return [task.to_dict() for task in tasks]


