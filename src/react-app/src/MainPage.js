import './App.css';
import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faKey, faTrash } from '@fortawesome/free-solid-svg-icons';
import "bootstrap/dist/css/bootstrap.min.css";
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import { GrSearchAdvanced } from "react-icons/gr";
import { FaArrowDown, FaExpand } from "react-icons/fa";
import { CgMinimize } from "react-icons/cg";
import { PiMagnifyingGlassMinus } from "react-icons/pi";
import { MdExpandMore } from "react-icons/md";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';

function MainPage({ openaiKey, creds }) {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [showOptions, setShowOptions] = useState(false);
  const [activeKeys, setActiveKeys] = useState([]);
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (inputRef.current && window.innerWidth < 768) {
      inputRef.current.scrollIntoView({ behavior: 'smooth' });
      inputRef.current.focus();
    }
  }, []);

  const fetchResults = async (newPage) => {
    setIsLoading(true);
    try {
      const response = await fetch(`https://ff2hzmpmc5.us-east-1.awsapprunner.com/query?page=${newPage}&limit=10`, {
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
        setActiveKeys(data.result.map((_, i) => i.toString()));
      } else {
        setResponse(prev => [...prev, ...data.result]);
        setActiveKeys(prev => [...prev, ...data.result.map((_, i) => (i + page * 10).toString())]);
      }
      setHasMore(data.result?.length === 10);
      setPage(newPage);
    } catch (err) {
      console.error("Query failed:", err);
      setResponse(["Failed to fetch data."]);
    }
    setIsLoading(false);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setResponse([]);
    setPage(1);
    setHasMore(true);
    setActiveKeys([]);
    setHistory(prev => [...new Set([query, ...prev])]);
    await fetchResults(1);
  };

  const handleLoadMore = () => {
    fetchResults(page + 1);
  };

  const expandAll = () => {
    setActiveKeys(response.map((_, i) => i.toString()));
  };

  const collapseAll = () => {
    setActiveKeys([]);
  };

  const toggleKey = (key) => {
    setActiveKeys(prev =>
      prev.includes(key) ? prev.filter(k => k !== key) : [...prev, key]
    );
  };

  const clearResults = () => {
    setQuery("");
    setResponse([]);
    setPage(1);
    setHasMore(false);
    setActiveKeys([]);
  };

  const renderMultimedia = (url) => {
    if (!url) return null;
    const fileExtension = url.split('.').pop().split('?')[0].toLowerCase();
    if (["jpg", "jpeg", "png", "gif", "webp"].includes(fileExtension)) {
      return <img src={url} alt="media" className="media-img" />;
    } else if (["mp4", "webm", "ogg"].includes(fileExtension)) {
      return (
        <video controls className="media-video">
          <source src={url} type={`video/${fileExtension}`} />
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

  const disabled = !query.trim() || !creds?.accessKeyId || !openaiKey;

  const filtered = response.filter(item =>
    typeof item === "string" || JSON.stringify(item).toLowerCase().includes(searchTerm)
  );

  return (
    <div className="main-content">
      <video autoPlay loop muted playsInline className="video-background">
        <source src="/mv.mp4" type="video/mp4" />
      </video>
      <div className="container text-center mt-5 pt-4 bg-black bg-opacity-75">
        {(!creds.accessKeyId || !openaiKey) ? (
          <small className="d-block mb-2">
            Please authenticate:
            <Link className="nav-link" to="/auth">
              <FontAwesomeIcon icon={faKey} />
            </Link>
          </small>
        ) : (
          <p className="lead">What skills would you like to see?</p>
        )}

        <form onSubmit={handleSubmit} className="d-flex justify-content-center mb-3">
          <input
            ref={inputRef}
            placeholder="Enter query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="form-control form-control-sm w-100"
          />
          <button type="submit" className="btn btn-outline-light ms-2" disabled={disabled}>
            <FaArrowDown />
          </button>
        </form>

        <div className="d-flex gap-2 justify-content-center mb-2">
          <OverlayTrigger
            placement="bottom"
            overlay={<Tooltip id="tooltip-advanced">Advanced</Tooltip>}
          >
            <button className="btn btn-outline-light btn-sm" onClick={() => setShowOptions(prev => !prev)}>
              {!showOptions ? <GrSearchAdvanced /> : <PiMagnifyingGlassMinus />}
            </button>
          </OverlayTrigger>
          <OverlayTrigger
            placement="bottom"
            overlay={<Tooltip id="tooltip-advanced">Expand All</Tooltip>}
          >
            <button className="btn btn-outline-light btn-sm" onClick={expandAll}><FaExpand /></button>
          </OverlayTrigger>
          <OverlayTrigger
            placement="bottom"
            overlay={<Tooltip id="tooltip-advanced">Collapse All</Tooltip>}
          >
            <button className="btn btn-outline-light btn-sm" onClick={collapseAll}><CgMinimize /></button>
          </OverlayTrigger>
        </div>

        {showOptions && (
          <div className="advanced-controls d-flex gap-2 mb-3 flex-column align-items-center">
            <select onChange={(e) => setQuery(e.target.value)} className="form-select form-select-sm w-100">
              <option value="">-- Query History --</option>
              {history.map((q, i) => <option key={i}>{q}</option>)}
            </select>
            <input
              placeholder="Filter current results..."
              onChange={(e) => setSearchTerm(e.target.value.toLowerCase())}
              className="form-control form-control-sm w-100"
            />
            <button onClick={clearResults} className="btn btn-outline-danger btn-sm w-100">
              <FontAwesomeIcon icon={faTrash} /> Clear Results
            </button>
          </div>
        )}

        <div className="results-container">
          {filtered.length > 0 &&
            filtered.map((item, index) => (
              typeof item === "string" ? (
                <div key={index}>{item}</div>
              ) : (
                <Accordion activeKey={activeKeys} alwaysOpen key={index}>
                  <Accordion.Item eventKey={index.toString()}>
                    <Accordion.Header onClick={() => toggleKey(index.toString())}>
                      <h6>{item.name || ""}</h6>
                    </Accordion.Header>
                    <Accordion.Body>
                      {item.image_s3_url && (
                        <div className="media-container">
                          {renderMultimedia(item.image_s3_url)}
                        </div>
                      )}
                      <br />
                      <ul>
                        {Object.entries(item).map(([key, value]) => {
                          if (key !== "name" && key !== "image_s3_url") {
                            return (
                              <li key={key}>
                                <strong>{key.replace(/_/g, " ")}:</strong> {value.toString()}
                              </li>
                            );
                          }
                          return null;
                        })}
                      </ul>
                    </Accordion.Body>
                  </Accordion.Item>
                </Accordion>
              )
            ))
          }
        </div>

        {hasMore && !isLoading && (
          <button onClick={handleLoadMore} className="btn btn-outline-light mt-3 load-more-btn">
            <OverlayTrigger
              placement="top"
              overlay={<Tooltip id="tooltip-advanced">Load More</Tooltip>}
            >
              <MdExpandMore />
            </OverlayTrigger>
          </button>
        )}
        {isLoading && (
          <div className="loading-overlay"><Spinner /></div>
        )}
      </div>
    </div>
  );
}

export default MainPage;