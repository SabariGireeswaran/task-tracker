import { useEffect, useState } from "react";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import FilterBar from "./components/FilterBar";
import Login from "./Login";

const API = import.meta.env.VITE_API_URL;
function App() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState(null);
  const [lastError, setLastError] = useState("");
  const[loggedIn, setLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  const getAuthHeader = () => ({
    Authorization: `Bearer ${localStorage.getItem("token")}`
  });

  const captureError = async (res, context) => {
    const text = await res.text().catch(() => "");
    const detail = text || res.statusText || "Unknown error";
    setLastError(`${context}: ${res.status} ${detail}`);
  };

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
        await captureError(res, "Load tasks failed");
        return;
      }

      const data = await res.json();
      setTasks(data);
    } catch (err) {
      console.error(err);
      setTasks([]);
      setLastError(`Load tasks failed: ${err.message}`);
    }
  };

  useEffect(() => {
    if (loggedIn) loadTasks();
  }, [filter, loggedIn]);

  const addTask = async (text) => {
    const res = await fetch(`${API}/tasks`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json", 
        ...getAuthHeader() },
      body: JSON.stringify({ description: text })
    });
    if (!res.ok) {
      await captureError(res, "Add task failed");
      return;
    }
    loadTasks();
  };

  const deleteTask = async (id) => {
    const res = await fetch(`${API}/tasks/${id}`, {
      method: "DELETE",
      headers: getAuthHeader()
    });
    if (!res.ok) {
      await captureError(res, "Delete task failed");
      return;
    }
    loadTasks();
  };

  const toggleTask = async (task) => {
    const newStatus = task.status === "done" ? "todo" : "done";

    const res = await fetch(`${API}/tasks/${task.id}/status`, {
      method: "PUT",
      headers: { 
        "Content-Type": "application/json",
        ...getAuthHeader() 
      },
      body: JSON.stringify({ status: newStatus })
    });
    if (!res.ok) {
      await captureError(res, "Update status failed");
      return;
    }

    loadTasks();
  };
  
  const logout = () => {
    localStorage.removeItem("token");
    setLastError("");
    setLoggedIn(false);
  }

  if (!loggedIn) {
    return (
      <Login
        onLogin={() => setLoggedIn(true)}
        onError={(msg) => setLastError(msg)}
      />
    );
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>Task Tracker</h1>
      <div style={{ marginBottom: 16, fontSize: 14 }}>
        <div>API: {API}</div>
        <div>Token: {localStorage.getItem("token") ? "present" : "missing"}</div>
        <div>Last error: {lastError || "none"}</div>
      </div>

      <TaskForm onAdd={addTask} />
      <TaskList tasks={tasks} onDelete={deleteTask} onToggle={toggleTask} />
      <FilterBar setFilter={setFilter} />
      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default App;
