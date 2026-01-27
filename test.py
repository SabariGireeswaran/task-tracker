from core.task import Task

t=Task(1,"Learn OOPS  +  LLD")
print(t.to_dict())

t.mark_status("in-progress")
print(t.to_dict())