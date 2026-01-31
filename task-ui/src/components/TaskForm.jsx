import { useState } from "react";

export default function TaskForm({ onAdd }) {
    const [text, setText] = useState("");

    const handleAdd = () => {
        if (!text.trim()) return;
        onAdd(text);
        setText("");
    };

    return (
        <div style = {{marginBottom: 20}}>
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter task..."
            />
            <button onClick={handleAdd}>Add</button>
        </div>
    );
}