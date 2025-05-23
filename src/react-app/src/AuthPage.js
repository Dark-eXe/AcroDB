import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AiFillOpenAI } from "react-icons/ai";
import { FaAws } from "react-icons/fa";

function AuthPage({ openaiKey, setOpenaiKey, handleLogin, creds }) {
  const [showApiModal, setShowApiModal] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const storedKey = sessionStorage.getItem("openai_api_key");
    const openaiReady = storedKey || openaiKey;

    if (creds?.accessKeyId && openaiReady) {
      console.log("✅ Redirecting with creds:", creds);
      navigate("/", { replace: true });
    }
  }, [creds, openaiKey, navigate]);


  const handleSaveApiKey = () => {
    sessionStorage.setItem("openai_api_key", openaiKey);
    setShowApiModal(false);
  };

  return (
    <div className="main-content">
      <video
				autoPlay
				loop
				muted
				playsInline
				className="video-background"
			>
				<source src="/mv.mp4" type="video/mp4" />
				Your browser does not support the video tag.
			</video>

      <div className="container text-center mt-5 text-white bg-black bg-opacity-75">
        <br />
        <h6>Authenticate with AWS and OpenAI Credentials</h6> <br />

        {!creds?.accessKeyId && (
          <button className="btn btn-outline-warning btn-lg mb-3" onClick={handleLogin}>
            <FaAws />
          </button>
        )}

        {creds?.accessKeyId && (
          <div className="btn btn-outline-success btn-lg mb-3">
            <FaAws />
          </div>
        )}

        <button
          className={`btn btn-lg mb-2 ${openaiKey ? "btn-outline-success" : "btn-outline-warning"}`}
          onClick={() => setShowApiModal(true)}
        >
          <AiFillOpenAI />
        </button>

        {showApiModal && (
          <div className="modal show fade d-block" tabIndex="-1" role="dialog" style={{ backgroundColor: "rgba(0,0,0,0.5)" }}>
            <div className="modal-dialog modal-dialog-centered">
              <div className="modal-content bg-black border border-white border-opacity-50 text-white">
                <div className="modal-header">
                  <AiFillOpenAI />
                  <button type="button" className="btn-close btn-close-white" onClick={() => setShowApiModal(false)}></button>
                </div>
                <div className="modal-body">
                  <input
                    type="password"
                    className="form-control"
                    placeholder="API Key"
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

        <br />
      </div>
    </div>
  );
}

export default AuthPage;
