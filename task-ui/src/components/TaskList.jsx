import TaskItem from "./TaskItem";

export default function TaskList({ tasks,oneDelete, onToggle }) {
    return (
        <div>
            {tasks.map(t => (
                <TaskItem
                  key={t.id}
                  task={t}
                  OnDelete={onDelete}
                  OnToggle={onToggle}
                />
            ))}
        </div>
    );
}