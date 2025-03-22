import './App.css';
import { useState} from "react";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch("http://127.0.0.1:8000/query", {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    const data = await response.json();
    setResponse(data.result);
  };

  return (
    <div>
        <h1>AcroDB</h1>
        <h2>Chat Query</h2>
        <form onSubmit={handleSubmit}>
        <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Enter query..." />
        <button type="submit">Send</button>
      </form>
      <pre>{response ? response : "No response yet"}</pre>
    </div>
  );
}

export default App;
