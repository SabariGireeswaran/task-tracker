from core.task import Task


class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    # -------------------------
    # Create
    # -------------------------
    def add_task(self, description: str, user_id: int):
        return self.storage.add(description, user_id)

    # -------------------------
    # Read
    # -------------------------
    def list_tasks(self, status=None, user_id=None):
        tasks = self.storage.load(user_id)

        if status:
            tasks = [t for t in tasks if t["status"] == status]

        return tasks

    def get_task_by_id(self, task_id: int, user_id: int):
        tasks = self.storage.load(user_id)

        for t in tasks:
            if t["id"] == task_id:
                return t

        return None

    # -------------------------
    # Update
    # -------------------------
    def update_task(self, task_id, description, user_id):
        return self.storage.update(task_id, description, user_id)

    def mark_task(self, task_id, status, user_id):
        return self.storage.update_status(task_id, status, user_id)

    # -------------------------
    # Delete
    # -------------------------
    def delete_task(self, task_id, user_id):
        return self.storage.delete(task_id, user_id)