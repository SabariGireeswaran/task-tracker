# task_cli.py
# A command-line interface for managing tasks in a task tracker application.
# It allows users to add, list, update, delete, and mark tasks with different statuses.
# The tasks are stored in a JSON file for persistence.
# Required imports
import json
import os
import sys
from datetime import datetime
from core.manager import TaskManager
from storage.json_store import JsonTaskStore

store = JsonTaskStore("tasks.json")
manager = TaskManager(store)

TASKS_FILE = "tasks.json"
def parse_task_id(value):
    try:
        return int(value)
    except ValueError:
        print("Error: Task ID must be a number.")
        return None

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

def mark_task_status(task_id, new_status):
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return
    
    task["status"] = new_status
    task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_tasks(tasks)
    print(f"Task {task_id} marked as {new_status}.")
def print_usage():
    print("""
                Task Tracker CLI - Usage:

    add "description"             Add a new task   
    update <id> "description"     Update a task
    delete <id>                   Delete a task
    list                          List all tasks
    list todo|done|in-progress    List tasks by status
    mark-in-progress <id>         Mark task as in-progress
    markdone <id>                 Mark task as done
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [<args>]")
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "add":  # Add a new task
        if len(sys.argv) < 3:
            print("Usage: task-cli add \"description\"")
            sys.exit(1)
        
        task = manager.add_task(sys.argv[2])
        print(f"Task added successfully (ID: {task.id})")

    elif command == "list": # List tasks
        status = sys.argv[2] if len(sys.argv) > 2 else None
        tasks = manager.list_tasks(status)

        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                print(task.to_dict())

    elif command == "update":  # Update a task
        if len(sys.argv) < 4:
            print("Usage: task-cli update <id> \"new description\"")
        try:
            manager.update_task(int(sys.argv[2]), sys.argv[3])
            print(f"Task updated successfully.")
        except ValueError as e:
            print(e)

    elif command == "delete":   # Delete a task
        if len(sys.argv) < 3:
            print("Usage: task-cli delete <id>")
            sys.exit(1)
        try:
            manager.delete_task(int(sys.argv[2]))
            print("Task deleted successfully.")
        except ValueError as e:
            print(e)

    elif command == "mark-in-progress":  # Mark task as in-progress
        try:
            manager.mark_task(int(sys.argv[2]), "in-progress")
            print("Task marked as in-progress.")
        except ValueError as e:
            print(e)

    elif command == "mark-done":  # Mark task as done
        try:
            manager.mark_task(int(sys.argv[2]), "done")
            print("Task marked as done.")
        except ValueError as e:
            print(e)
    else:
        print(f"Unknown command: {command}")

    