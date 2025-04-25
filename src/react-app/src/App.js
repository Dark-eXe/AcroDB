import './App.css';
import { useState } from "react";
import { useEffect } from "react";
import { CognitoIdentityCredentials, config } from "aws-sdk";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [openaiKey, setOpenaiKey] = useState(sessionStorage.getItem("openai_api_key") || "");
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);
  const [showApiModal, setShowApiModal] = useState(false);
  useEffect(() => {
    const hash = window.location.hash;
    if (hash.includes("id_token")) {
      const idToken = new URLSearchParams(hash.replace("#", "?")).get("id_token");
  
      sessionStorage.setItem("cognito_id_token", idToken);
  
      config.region = "us-east-1";
      config.credentials = new CognitoIdentityCredentials({
        IdentityPoolId: "us-east-1:d61e5ada-6ae3-4670-b58d-16666fee8379",
        Logins: {
          "cognito-idp.us-east-1.amazonaws.com/us-east-1_wFEVP6OdC": idToken
        }        
      });
  
      config.credentials.get((err) => {
        if (!err) {
          const creds = {
            accessKeyId: config.credentials.accessKeyId,
            secretAccessKey: config.credentials.secretAccessKey,
            sessionToken: config.credentials.sessionToken,
          };
          sessionStorage.setItem("aws_creds", JSON.stringify(creds));
          window.history.replaceState(null, "", window.location.pathname);
        } else {
          console.error("AWS credential error", err);
        }
      });
    }
  }, []);
  
  const handleLogin = () => {
    const loginUrl = `https://us-east-1wfevp6odc.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=2iv8mu5ivuvc7h0nb59vfdnfjp&redirect_uri=http://localhost:3000`;
    window.location.href = loginUrl;
  };

  const handleSaveApiKey = () => {
    sessionStorage.setItem("openai_api_key", openaiKey);
    setShowApiModal(false);
  };

  const fetchResults = async (newPage) => {
    const creds = JSON.parse(sessionStorage.getItem("aws_creds") || "{}");
    const openaiKey = sessionStorage.getItem("openai_api_key") || "";

    const response = await fetch(`http://127.0.0.1:8000/query?page=${newPage}&limit=5`, {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        aws_access_key_id: creds.accessKeyId,
        aws_secret_access_key: creds.secretAccessKey,
        aws_session_token: creds.sessionToken,
        openai_api_key: openaiKey
      })
    });

    const data = await response.json();

    if (newPage === 1) {
      setResponse(data.result);
    } else {
      setResponse((prevResults) => [...prevResults, ...data.result]);
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
    if (!url) return null;
    const fileExtension = url.split('.').pop().split('?')[0].toLowerCase();

    if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(fileExtension)) {
      return <img src={url} alt="media" className="media-img" />;
    } else if (['mp4', 'webm', 'ogg'].includes(fileExtension)) {
      return (
        <video controls className="media-video">
          <source src={url} type={`video/${fileExtension}`} />
          Your browser does not support the video tag.
        </video>
      );
    } else if (fileExtension === 'pdf') {
      return <iframe src={url} className="media-pdf" title="PDF Viewer"></iframe>;
    } else if (fileExtension === 'txt') {
      return <a href={url} target="_blank" rel="noopener noreferrer">View Text File</a>;
    } else {
      return <a href={url} download>{url}</a>;
    }
  };

  const creds = JSON.parse(sessionStorage.getItem("aws_creds") || "{}");
  const disabled = !query.trim() || !creds.accessKeyId || !openaiKey;

  return (
    <div>
      {/* Video background */}
      <video autoPlay loop muted className="video-background">
        <source src="/mv.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {/* Container */}
      <div className="container text-center mt-2 fixed-top bg-black bg-opacity-75">
        {/* Header */}
        <div className="jumbotron">
          <h1 className="display-4 text-warning">Acro<span className="display-4 text-white">DB</span></h1>
          <p className="lead">Chat-queried NoSQL database for gymnasts and parkour practitioners.</p>
          <hr className="my-4" />
        </div>

        <small className="d-block mb-2" style={{ color: "#ccc" }}>
          Access database with AWS and OpenAI.<br/>
        </small>

        {!creds.accessKeyId && (
          <button className="btn btn-success mb-3" onClick={handleLogin}>
            Login with AWS Cognito
          </button>
        )}

        {creds.accessKeyId && (
          <div className="text-success mb-3">Logged in via AWS Cognito</div>
        )}

        <button
          className={`btn mb-2 ${openaiKey ? "btn-outline-success" : "btn-outline-warning"}`}
          onClick={() => setShowApiModal(true)}
        >
          {openaiKey ? "OpenAI set" : "Set OpenAI API Key"}
        </button>
        <small className="d-block mb-2" style={{ color: "#ccc" }}>
          <em>Your key stays in your browser and is never sent to our servers.</em>
        </small>

        {showApiModal && (
          <div className="modal show fade d-block" tabIndex="-1" role="dialog" style={{ backgroundColor: "rgba(0,0,0,0.5)", overflow: "hidden" }}>
            <div className="modal-dialog modal-dialog-centered">
              <div className="modal-content bg-dark text-white">
                <div className="modal-header">
                  <h5 className="modal-title">Enter OpenAI API Key</h5>
                  <button type="button" className="btn-close btn-close-white" onClick={() => setShowApiModal(false)}></button>
                </div>
                <div className="modal-body">
                  <input
                    type="password"
                    className="form-control"
                    placeholder="OpenAI API Key"
                    value={openaiKey}
                    onChange={(e) => setOpenaiKey(e.target.value)}
                  />
                </div>
                <div className="modal-footer">
                  <button className="btn btn-secondary" onClick={() => setShowApiModal(false)}>Cancel</button>
                  <button className="btn btn-primary" onClick={handleSaveApiKey}>Save</button>
                </div>
              </div>
            </div>
          </div>
        )}

        <div style={{
          width: "75%",
          height: "1px",
          backgroundColor: "#ccc",
          opacity: 0.7,
          margin: "1rem 0"
        }} />
        <p className="lead">What acrobatic skills are you looking for?</p>


        {/* Query Form */}
        <form onSubmit={handleSubmit} className="d-flex justify-content-center mb-3">
          <input
            placeholder="Enter query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="form-control form-control-sm w-100"
          />
          <button type="submit" className="btn btn-outline-light ms-2" disabled={disabled}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-arrow-down" viewBox="0 0 16 16">
              <path fillRule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1" />
            </svg>
          </button>
        </form>

        {/* Response */}
        <div className="response-container">
          {response.length > 0 &&
            response.map((item, index) => (
              typeof item === "string" ? (
                <div key={index}>{item}</div>
              ) : (
                <div key={index} className="card text-white bg-dark mb-3">
                  <div className="card-body">
                    <h5 className="card-title">{item.name || ""}</h5>
                    {item.image_s3_url && (
                      <div className="media-container">
                        {renderMultimedia(item.image_s3_url)}
                      </div>
                    )}
                    <ul className="list-group list-group-flush">
                      {Object.entries(item).map(([key, value]) => {
                        if (key !== "name" && key !== "image_s3_url") {
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
          }
        </div>

        {/* Pagination */}
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