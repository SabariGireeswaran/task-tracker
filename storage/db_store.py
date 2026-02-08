from sqlalchemy.orm import Session
from storage.db.database import SessionLocal
from storage.db.models import Task as TaskModel


class DbTaskStore:

    def load(self, user_id):
        db: Session = SessionLocal()

        tasks = db.query(TaskModel).filter(TaskModel.user_id == user_id).all()

        result = [
            {
                "id": t.id,
                "description": t.description,
                "status": t.status,
                "user_id": t.user_id
            }
            for t in tasks
        ]

        db.close()
        return result


    def add(self, description, user_id):
        db = SessionLocal()

        task = TaskModel(
            description=description,
            status="todo",
            user_id=user_id
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        result = {
            "id": task.id,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id
        }

        db.close()
        return result


    def update(self, task_id, description, user_id):
        db = SessionLocal()

        task = db.query(TaskModel).filter(
            TaskModel.id == task_id,
            TaskModel.user_id == user_id
        ).first()

        if task:
            task.description = description
            db.commit()

        db.close()


    def update_status(self, task_id, status, user_id):
        db = SessionLocal()

        task = db.query(TaskModel).filter(
            TaskModel.id == task_id,
            TaskModel.user_id == user_id
        ).first()

        if task:
            task.status = status
            db.commit()

        db.close()


    def delete(self, task_id, user_id):
        db = SessionLocal()

        task = db.query(TaskModel).filter(
            TaskModel.id == task_id,
            TaskModel.user_id == user_id
        ).first()

        if task:
            db.delete(task)
            db.commit()

        db.close()
