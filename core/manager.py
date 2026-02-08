class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    # CREATE
    def add_task(self, description: str, user_id: int):
        return self.storage.add(description, user_id)

    # READ
    def list_tasks(self, status=None, user_id=None):
        return self.storage.load(user_id)

    def get_task_by_id(self, task_id, user_id):
        tasks = self.storage.load(user_id)
        for t in tasks:
            if t["id"] == task_id:
                return t
        return None

    # UPDATE
    def update_task(self, task_id, description, user_id):
        return self.storage.update(task_id, description, user_id)

    def mark_task(self, task_id, status, user_id):
        return self.storage.update_status(task_id, status, user_id)

    # DELETE
    def delete_task(self, task_id, user_id):
        return self.storage.delete(task_id, user_id)
