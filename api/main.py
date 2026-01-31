from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from core.manager import TaskManager
from storage.db_store import DbTaskStore

from storage.db.database import engine, Base
from storage.db import models

from fastapi.responses import RedirectResponse

app = FastAPI(
    title = "Task Tracker API",
    description="Simple task manager built with FastAPI + Clean Architecture",
    version="1.0.0"    
)

# Create database tables
Base.metadata.create_all(bind=engine)

# ---- Dependency setup (same as CLI) ---- 
store = DbTaskStore()
manager = TaskManager(store)

# ---- Request schema FIRST ----
class TaskCreate(BaseModel):

    description: str

class TaskUpdate(BaseModel):
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
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url = "/docs")

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
    tasks = manager.list_tasks(task_status)

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

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):

    if not task.description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description cannot be empty"
        )
    
    try:
        manager.update_task(task_id, task.description)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    updated_task = manager.get_task_by_id(task_id)
    return updated_task.to_dict()
