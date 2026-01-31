export default function FilterBar({ setFilter }) {
    return(
        <div style={{ marginTop: 20 }}>
            <button onClick={() => setFilter(null)}>All</button>
            <button onClick={() => setFilter("todo")}>Todo</button>
            <button onClick={() => setFilter("in-progress")}>In Progress</button>
            <button onClick={() => setFilter("done")}>Done</button>
        </div>
    );
}