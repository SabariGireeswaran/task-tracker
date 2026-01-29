from fastapi import FastAPI, HTTPException, status
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

@app.post("/tasks", response_model = TaskResponse,
          status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    if not task.description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description cannot be empty"
        )
    
    new_task = manager.add_task(task.description)
    return new_task.to_dict()

VALID_STATUSES = {"todo", "in-progress", "done"}

@app.get("/tasks")
def list_tasks(task_status: str | None = None):
    if task_status is not None and task_status not in VALID_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Allowed values: {', '.join(VALID_STATUSES)}"
        )
    try:
        tasks = manager.list_tasks(status)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tasks found"
        )   
    
    return [task.to_dict() for task in tasks]

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = manager.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return task.to_dict()

