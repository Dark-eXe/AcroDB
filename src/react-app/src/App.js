import './App.css';
import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

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

  const renderMultimedia = (url) => {
    if (!url) return null; // No multimedia
  
    const fileExtension = url.split('.').pop().split('?')[0].toLowerCase(); // Extract file type
  
    if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(fileExtension)) {
      return <img src={url} alt="media" className="media-img" />;
    } 
    else if (['mp4', 'webm', 'ogg'].includes(fileExtension)) {
      return <video controls className="media-video">
        <source src={url} type={`video/${fileExtension}`} />
        Your browser does not support the video tag.
      </video>;
    } 
    else if (fileExtension === 'pdf') {
      return <iframe src={url} className="media-pdf" title="PDF Viewer"></iframe>;
    } 
    else if (fileExtension === 'txt') {
      return <a href={url} target="_blank" rel="noopener noreferrer">View Text File</a>;
    } 
    else {
      return <a href={url} download>{url}</a>;
    }
  };
  

  return (
    <div>
      {/*video background*/}
      <video autoPlay loop muted className="video-background">
          <source src="/mv.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>

      {/*container*/}
      <div className="container text-center mt-2 fixed-top bg-black bg-opacity-75">
        {/*header*/}
        <div class="jumbotron">
          <h1 class="display-4 text-warning">Acro<span class="display-4 text-white">DB</span></h1>
          <p class="lead">Chat-queried NoSQL database for gymnastics & parkour skills using AWS and OpenAI.</p>
          <hr class="my-4"/>
          <p class="lead">What acrobatic skills are you looking for?</p>
        </div>

        {/*query*/}
        <div className="">
          {/*form*/}
          <form onSubmit={handleSubmit} className="d-flex justify-content-center mb-3">
            <input 
              placeholder="Enter query..."
              class="form-control w-100"
              value={query} 
              onChange={(event) => setQuery(event.target.value)} 
              className="form-control form-control-sm w-100"
            />
            <button type="submit" className="btn btn-outline-light ms-2 " disabled={!query.trim()}>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-down" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1"/>
              </svg>
            </button>
          </form>

          {/*response*/}
          <div className="response-container">
            {response.length > 0 ? (
              response.map((item, index) => (
                typeof item === "string" ? (  // Handle raw string responses separately
                  <div key={index} className="">{item}</div>
                ) : (
                  <div key={index} className="card text-white bg-dark mb-3">
                    <div className="card-body">
                      <h5 className="card-title">{item.name || ""}</h5>

                      {/* Optional Multimedia */}
                      {item.image_s3_url && (
                        <div className="media-container">
                          {renderMultimedia(item.image_s3_url)}
                        </div>
                      )}

                      {/* Dynamically render available attributes */}
                      <ul className="list-group list-group-flush">
                        {Object.entries(item).map(([key, value]) => {
                          if (key !== "name" && key !== "image_s3_url") {  // Exclude title & image
                            return (
                              <li key={key} className="list-group-item bg-dark text-white">
                                <strong>{key.replace(/_/g, " ")}:</strong> {value.toString()}
                              </li>
                            );
                          }
                          return null;
                        })}
                      </ul>
                    </div>
                  </div>
                )
              ))
            ) : ""
            }
          </div>

          {/*pagination*/}
          {hasMore && (
            <button onClick={handleLoadMore} className="btn btn-outline-light mt-3">
              Load More
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
