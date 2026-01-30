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
        
        #Clear table first(simple approach Like JSON overwrite)
        db.query(TaskModel).delete()

        for item in data:
            task = TaskModel(**item)
            db.add(task)
        
        db.commit()
        db.close()
        