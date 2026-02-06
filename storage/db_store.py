from sqlalchemy.orm import Session
from storage.db.database import SessionLocal
from storage.db.models import Task as TaskModel

class DbTaskStore:
    def load(self):
        db: Session = SessionLocal()
        tasks = db.query(TaskModel).all()

        result = []
        for t in tasks:
            result.append({
                "id": t.id,
                "description": t.description,
                "status": t.status,
                "createdAt": t.createdAt,
                "updatedAt": t.updatedAt
            })       
        db.close()
        return result

    def save(self, data):
        db: Session = SessionLocal()
        ids = {item["id"] for item in data}

        if ids:
            db.query(TaskModel).filter(~TaskModel.id.in_(ids)).delete(synchronize_session=False)
        else:
            db.query(TaskModel).delete(synchronize_session=False)
        
        for item in data:
            task = db.get(TaskModel, item["id"])
            if task:
                task.description = item["description"]
                task.status = item["status"]
                task.createdAt = item["createdAt"]
                task.updatedAt = item["updatedAt"]
            else:
                task = TaskModel(**item)
                db.add(task)

        db.commit()
        db.close()
        
