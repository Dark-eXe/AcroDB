import './App.css';
import { useState, useEffect, useRef } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

// const videos = ["/mv1.mp4", "/mv2.mp4", "/mv3.mp4"];

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState([]);
  const [page, setPage] = useState(1); // current page
  const [hasMore, setHasMore] = useState(false);

  const fetchResults = async (newPage) => {
    const response = await fetch(`http://127.0.0.1:8000/query?page=${newPage}&limit=5`, {
      method: 'POST',
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ query })
    });
    const data = await response.json();

    if (newPage === 1) {
      setResponse(data.result); // Reset results if it's a new search
    } else {
      setResponse((prevResults) => [...prevResults, ...data.result]); // Append results
    }

    setHasMore(data.result.length === 5);
    setPage(newPage);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setResponse([]);
    setPage(1);
    setHasMore(true);
    await fetchResults(1);
  };

  const handleLoadMore = () => {
    fetchResults(page + 1);
  };

  return (
    <div className="container text-center mt-2 fixed-top bg-white bg-opacity-10 bg-gradient">
      <video autoPlay loop muted className="video-background">
        <source src="/mv.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>


      <header className="pb-5 text-white" >
        <h1>AcroDB</h1>
        <h6>Chat-queried NoSQL database for gymnastics & parkour skills using AWS and OpenAI.</h6>
      </header>

      <div className="">
        <form onSubmit={handleSubmit} className="d-flex justify-content-center mb-3">
          <input 
            value={query} 
            onChange={(event) => setQuery(event.target.value)} 
            placeholder="Enter query..."
            className="form-control form-control-sm w-100"
          />
          <button type="submit" className="btn btn-outline-light ms-2">Send</button>
        </form>

        <pre className="text-light">
          {response.length ? response.map((item, index) => (
            <div key={index}>{item}</div>
          )) : ""}
        </pre>

        {hasMore && (
          <button onClick={handleLoadMore} className="btn btn-outline-light mt-3">
            Load More
          </button>
        )}
      </div>

    </div>
  );
}

export default App;
