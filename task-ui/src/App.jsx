import { useEffect, useState } from "react";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import FilterBar from "./components/FilterBar";
import Login from "./Login";

const API = "https://task-tracker-23ld.onrender.com"; // ⭐ MUST BE HERE (TOP LEVEL)

function App() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState(null);
  const[loggedIn, setLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  const getAuthHeader = () => ({
    Authorization: `Bearer ${localStorage.getItem("token")}`
  });

  const loadTasks = async () => {
    try{
      const url = filter 
      ? `${API}/tasks?task_status=${filter}`
      : `${API}/tasks`;

      const res = await fetch(url, {
        headers: getAuthHeader()
      });

      if (!res.ok) {
        setTasks([]);
        return;
      }

      const data = await res.json();
      setTasks(data);
    } catch (err) {
      console.error(err);
      setTasks([]);
    }
  };

  useEffect(() => {
    if (loggedIn) loadTasks();
  }, [filter, loggedIn]);

  const addTask = async (text) => {
    await fetch(`${API}/tasks`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json", 
        ...getAuthHeader() },
      body: JSON.stringify({ description: text })
    });
    loadTasks();
  };

  const deleteTask = async (id) => {
    await fetch(`${API}/tasks/${id}`, {
      method: "DELETE",
      headers: getAuthHeader()
    });
    loadTasks();
  };

  const toggleTask = async (task) => {
    const newStatus = task.status === "done" ? "todo" : "done";

    await fetch(`${API}/tasks/${task.id}/status`, {
      method: "PUT",
      headers: { 
        "Content-Type": "application/json",
        ...getAuthHeader() 
      },
      body: JSON.stringify({ status: newStatus })
    });

    loadTasks();
  };
  
  const logout = () => {
    localStorage.removeItem("token");
    setLoggedIn(false);
  }

  if (!loggedIn) {
    return <Login onLogin={() => setLoggedIn(true)}/>;
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>Task Tracker</h1>

      <TaskForm onAdd={addTask} />
      <TaskList tasks={tasks} onDelete={deleteTask} onToggle={toggleTask} />
      <FilterBar setFilter={setFilter} />
      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default App;
