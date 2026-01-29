from core.task import Task


class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    def _load_tasks(self):
        data = self.storage.load()
        return [Task.from_dict(item) for item in data]
    
    def _save_tasks(self, tasks):
        data = [task.to_dict() for task in tasks]
        self.storage.save(data)
    
    def add_task(self, description):
        tasks = self._load_tasks()

        new_id = 1 if not tasks else tasks[-1].id + 1
        task = Task(task_id=new_id, description=description)
        
        tasks.append(task)
        self._save_tasks(tasks)

        return task
    
    def _find_task(self, tasks, task_id):
        for task in tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id, new_description):
        tasks = self._load_tasks()
        task = self._find_task(tasks, task_id)

        if task is None:
            raise ValueError("Task not found")
        
        task.update_description(new_description)
        self._save_tasks(tasks)

    def delete_task(self, task_id):
        tasks = self._load_tasks()
        task = self._find_task(tasks, task_id)

        if task is None:
            raise ValueError("Task not found")
        
        tasks.remove(task)
        self._save_tasks(tasks)

    def mark_task(self, task_id, status):
        tasks = self._load_tasks()
        task = self._find_task(tasks, task_id)

        if task is None:
            raise ValueError("Task not found")
        
        task.mark_status(status)
        self._save_tasks(tasks)

    def list_tasks(self, status = None):
        tasks = self._load_tasks()
        
        if status:
            return [t for t in tasks if t.status == status]
        
        return tasks
    
    def get_task_by_id(self, task_id: int):
        tasks = self._load_tasks()

        for task in tasks:
            if task.id == task_id:
                return task
            
        return None