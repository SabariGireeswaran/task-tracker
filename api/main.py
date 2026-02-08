from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from core.jwt_auth import create_access_token
from core.manager import TaskManager
from storage.db_store import DbTaskStore

from storage.db.database import engine, Base
from storage.db import models

from fastapi.responses import RedirectResponse

from storage.db.database import SessionLocal
from storage.db.models import User
from core.security import hash_password
from core.security import verify_password

from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends
from core.deps import get_current_user

app = FastAPI(
    title = "Task Tracker API",
    description="Simple task manager built with FastAPI + Clean Architecture",
    version="1.0.0"    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173",
                   "https://task-tracker-hazel-eight.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

class TaskStatusUpdate(BaseModel):
    status: str

class TaskResponse(BaseModel):
    id: int
    description: str
    status: str

class MessageResponse(BaseModel):
    message: str

class UserCreate(BaseModel):
    username: str
    password: str

# ---- Routes AFTER ----
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url = "/docs")

@app.post("/tasks", response_model = TaskResponse,
          status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate,
                user: User = Depends(get_current_user)):
    if not task.description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description cannot be empty"
        )
    
    new_task = manager.add_task(task.description, user.id)
    return new_task

VALID_STATUSES = {"todo", "in-progress", "done"}

@app.get("/tasks")
def list_tasks(task_status: str | None = None,
               user: User = Depends(get_current_user)):
    if task_status is not None and task_status not in VALID_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Allowed values: {', '.join(VALID_STATUSES)}"
        )
    tasks = manager.list_tasks(task_status, user.id)

    return [task for task in tasks]

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int,
             user: str = Depends(get_current_user)):
    task = manager.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int,
                task: TaskUpdate,
                user: str = Depends(get_current_user)):

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
    return updated_task

@app.put("/tasks/{task_id}/status", response_model=TaskResponse)
def update_task_status(task_id: int, 
                       task: TaskStatusUpdate,
                       user: str = Depends(get_current_user)):
    if task.status not in VALID_STATUSES:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Invalid status. Allowed values: {','.join(VALID_STATUSES)}"
        )
    
    try:
        manager.mark_task(task_id, task.status)
    except ValueError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    updated_task = manager.get_task_by_id(task_id)
    return updated_task

@app.delete("/tasks/{task_id}", response_model=MessageResponse)
def delete_task(task_id: int,
                user: str = Depends(get_current_user)):

    try:
        manager.delete_task(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return {"message": f"Task {task_id} deleted successfully."}

@app.post("/register")
def register(user: UserCreate):
    db = SessionLocal()

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        db.close()
        raise HTTPException(400, "Username already exists")
    
    new_user = User(
        username = user.username,
        password = hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserCreate):
    db = SessionLocal()

    db_user = db.query(User).filter(User.username == user.username).first()
    db.close()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(401, "Invalid credentials")
    
    token = create_access_token({"sub": db_user.username})

    return{
        "access_token": token,
        "token_type": "bearer"
    }