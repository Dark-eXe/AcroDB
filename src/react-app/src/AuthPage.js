import React, { useState } from "react";

function AuthPage({ openaiKey, setOpenaiKey, handleLogin, creds }) {
  const [showApiModal, setShowApiModal] = useState(false);

  const handleSaveApiKey = () => {
    sessionStorage.setItem("openai_api_key", openaiKey);
    setShowApiModal(false);
  };

  return (
    <div>

        <div className="container text-center mt-5 text-white">
        <h2>Authentication</h2>
        <p>Access AcroDB using AWS and OpenAI credentials.</p>

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

        {showApiModal && (
            <div className="modal show fade d-block" tabIndex="-1" role="dialog" style={{ backgroundColor: "rgba(0,0,0,0.5)" }}>
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
        </div>

    </div>
  );
}

export default AuthPage;
