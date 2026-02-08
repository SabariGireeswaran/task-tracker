from sqlalchemy.orm import Session
from storage.db.database import SessionLocal
from storage.db.models import Task as TaskModel

class DbTaskStore:

    def load(self, user_id: int):
        db: Session = SessionLocal()

        tasks = (
            db.query(TaskModel)
            .filter(TaskModel.user_id == user_id)
            .all()
        )

        result = []

        for t in tasks:
            result.append({
                "id": t.id,
                "description": t.description,
                "status": t.status,
                "user_id": t.user_id
            })

        db.close()
        return result


    def save(self, data):
        db: Session = SessionLocal()

        for item in data:
            task = TaskModel(**item)
            db.add(task)

        db.commit()
        db.close()
