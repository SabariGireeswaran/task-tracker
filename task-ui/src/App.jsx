import { useEffect, useState } from "react";

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  //Load tasks from backend
  const loadTasks = () => {
    fetch("http://127.0.0.1:8000/tasks")
      .then(res => res.json())
      .then(data => setTasks(data))
      .catch(() => setTasks([]));
  };

  //run once on page load
  useEffect(() => {
    loadTasks();
  }, []);

  //Add task
  const addTask = async () => {
    if (!newTask.trim()) return;

    await fetch ("http://127.0.0.1:8000/tasks",{
      method: "POST",
      headers: { "Content-Type": "application/json"},
      body: JSON.stringify({ description: newTask })
    });

    setNewTask("");
    loadTasks(); //refresh list
  };
  
  useEffect(() => {
    fetch("http://127.0.0.1:8000/tasks")
      .then(res => {
        if (!res.ok) return [];
        return res.json();
      })
      .then(data => setTasks(data));
  }, []);

  return (
    <div style={{ padding: 40 }}>
      <h1>Task Tracker</h1>

      <input
        value={newTask}
        onChange={e => setNewTask(e.target.value)}
        placeholder="Enter task..."
      />

      <button onClick={addTask}>Add</button>

      <hr />

      {tasks.map(t => (
        <div key={t.id}>
          {t.description} - {t.status}
        </div>
      ))}
    </div>
  );
}

export default App;