import { useEffect,useState } from "react";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import FilterBar from "./components/FilterBar";

const API = "http://127.0.0.1:8000";

function App() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState(null);

  const loadTasks = () => {
    const url = filter ? `${API}/tasks?task_status=${filter}` : `${API}/tasks`;

    fetch(url)
      .then(res => res.json())
      .then(data => setTasks(data));
  };

  useEffect(() => {
    loadTasks();
  }, [filter]);

  const addTask = async (text) => {
    await fetch(`${API}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description: text })
    });
    loadTasks();
  };

  const deleteTask = async (id) => {
    await fetch(`${API}/tasks/${id}`, {method: "DELETE" });
    loadTasks();
  };

  const toggleTask = async (task) => {
    const newStatus = task.status === "done" ? "todo" : "done";

    await fetch(`${API}/tasks/${task.id}/status`,{
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus })
    });

    loadTasks();
  };

  return (
    <div style={{ padding: 40}}>
      <h1>Task Tracker</h1>

      <TaskForm onAdd={addTask} />
      <TaskList task={tasks} onDelete={deleteTask} onToggle={toggleTask} />
      <FilterBar setFilter={setFilter} />
    </div>
  )
}

export default App;