export default function TaskItem({ task, onDelete, onToggle}) {
    return (
        <div style={{
            display: "flex",
            gap: 10,
            marginBottom: 8
        }}>
            <input 
              type="checkbox"
              checked={task.status === "done"}
              onChange={() => onToggle(task)}
            />

            <span>{task.description}</span>

            <button onClick={() => onDelete(task.id)}>❌</button>
        </div>
    );
}