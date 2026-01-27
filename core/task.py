from datetime import datetime


class Task:
    def __init__(self, task_id, description, status="todo",
                 created_at=None, updated_at=None):
        self.id = task_id
        self.description = description
        self.status = status
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.created_at = created_at if created_at else now
        self.updated_at = updated_at if updated_at else now

    def update_description(self, new_description):
        self.description = new_description
        self._touch()

    def mark_status(self, new_status):
        self.status = new_status
        self._touch()
    
    def _touch(self):
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return{
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        return Task(
            task_id=data["id"],
            description = data["description"],
            status=data["status"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"]
        )
    