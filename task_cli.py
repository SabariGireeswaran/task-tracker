import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as file:
            json.dump([], file)
        return []

    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent = 4)

def add_task(description):
    tasks = load_tasks()
    
    new_id = 1 if not tasks else tasks[-1]["id"] + 1
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task added successfully (ID: {new_id})")

def list_tasks(filter_status = None):
    tasks = load_tasks()

    if not tasks: 
        print("No tasks found.")
        return

    for task in tasks:
        if filter_status is None or task["status"] == filter_status:
            print(f'[{task["id"]}] {task["description"]} ({task["status"]})')

def find_task_by_id(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def update_task(task_id, new_description):
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return
    task["description"] = new_description
    task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_tasks(tasks)
    print(f"Task {task_id} updated successfully.")
def delete_task(task_id):
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return
    
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [<args>]")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Task description is required.")
        else:
            description = sys.argv[2]
            add_task(description)
    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()
        else:
            status = sys.argv[2]
            if status not in ["todo", "done", "in-progress"]:
                print("Invalid status. Use: todo, done, in-progress")
            else:
                list_tasks(status)
    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: task-cli update <id> \"new description\"")
        else:
            task_id = int(sys.argv[2])
            new_description = sys.argv[3]
            update_task(task_id, new_description)
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: task-cli delete <id>")
        else:
            task_id = int(sys.argv[2])
            delete_task(task_id)
    else:
        print(f"Unknown command: {command}")

    