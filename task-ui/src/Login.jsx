import { useState } from "react";

const API = import.meta.env.VITE_API_URL;

export default function Login({ onLogin, onError }) {
    const[username, setUsername] = useState("");
    const[password, setPassword] = useState("");

    const handleLogin = async () => {
        try {
            const res = await fetch(`${API}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password  })
            });

            const data = await res.json().catch(() => ({}));
            if (!res.ok) {
                const detail = data?.detail ? ` (${data.detail})` : "";
                const msg = `Login failed${detail}`;
                onError?.(msg);
                alert(msg);
                return;
            }

            if (data.access_token) {
                localStorage.setItem("token", data.access_token);
                onLogin();
            } else {
                const msg = "Login failed (no token in response)";
                onError?.(msg);
                alert(msg);
            }
        } catch (err) {
            console.error(err);
            const msg = `Login failed (${err.message})`;
            onError?.(msg);
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
