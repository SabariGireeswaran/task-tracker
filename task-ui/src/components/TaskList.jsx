import TaskItem from "./TaskItem";

export default function TaskList({ tasks, onDelete, onToggle }) {
  return (
    <div>
      {tasks.map(t => (
        <TaskItem
          key={t.id}
          task={t}
          onDelete={onDelete}
          onToggle={onToggle}
        />
      ))}
    </div>
  );
}
