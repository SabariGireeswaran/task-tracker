import { useState } from "react";

const API ="http://127.0.0.1:8000"

export default function Login({ onLogin }) {
    const[username, setUsername] = useState("");
    const[password, setPassword] = useState("");

    const handleLogin = async () => {
        const res = await fetch(`${API}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password  })
        });

        const  data = await res.json();

        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            onLogin();
        } else {
            alert("Login failed");
        }
    };

    return (
        <div>
            <h2>Login</h2>
            
            <input placeholder="username" onChange={e => setUsername(e.target.value)}/>
            <input type="password" placeholder="password"
                onChange={e => setPassword(e.target.value)}/>

            <button onClick={handleLogin}>Login</button>
        </div>
    );
}