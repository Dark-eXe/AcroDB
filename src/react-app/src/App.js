import './App.css';
import { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation
} from "react-router-dom";
import { CognitoIdentityCredentials, config } from "aws-sdk";
import MainPage from "./MainPage";
import AuthPage from "./AuthPage";
import Navbar from "./Navbar";

function App() {
  return (
    <Router>
      <Navbar />
      <AppRoutes />
    </Router>
  );
}

function AppRoutes() {
  const [openaiKey, setOpenaiKey] = useState(sessionStorage.getItem("openai_api_key") || "");
  const [creds, setCreds] = useState({});
  const location = useLocation();  // <-- FIX: use react-router's location

  useEffect(() => {
    const hash = window.location.hash;

    if (location.pathname === "/auth" && hash.includes("id_token")) {
      const idToken = new URLSearchParams(hash.replace("#", "?")).get("id_token");
      sessionStorage.setItem("cognito_id_token", idToken);

      config.region = "us-east-1";
      config.credentials = new CognitoIdentityCredentials({
        IdentityPoolId: "us-east-1:d61e5ada-6ae3-4670-b58d-16666fee8379",
        Logins: {
          "cognito-idp.us-east-1.amazonaws.com/us-east-1_wFEVP6OdC": idToken,
        },
      });

      config.credentials.get((err) => {
        if (!err) {
          const newCreds = {
            accessKeyId: config.credentials.accessKeyId,
            secretAccessKey: config.credentials.secretAccessKey,
            sessionToken: config.credentials.sessionToken,
          };
          sessionStorage.setItem("aws_creds", JSON.stringify(newCreds));
          setCreds(newCreds);
          window.history.replaceState(null, "", location.pathname);
        } else {
          console.error("❌ AWS credential error:", err);
        }
      });
    } else {
      const storedCreds = sessionStorage.getItem("aws_creds");
      if (storedCreds) {
        const parsedCreds = JSON.parse(storedCreds);
        setCreds(parsedCreds);
      }
    }
  }, [location]);

  const handleLogin = () => {
    const loginUrl = `https://us-east-1wfevp6odc.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=2iv8mu5ivuvc7h0nb59vfdnfjp&redirect_uri=https://acrodb.io/auth`;
    window.location.href = loginUrl;
  };

  return (
    <Routes>
      <Route
        path="/auth"
        element={
          <AuthPage
            openaiKey={openaiKey}
            setOpenaiKey={setOpenaiKey}
            handleLogin={handleLogin}
            creds={creds}
          />
        }
      />
      <Route
        path="/"
        element={
          creds.accessKeyId && openaiKey
            ? <MainPage openaiKey={openaiKey} creds={creds} />
            : <Navigate to="/auth" replace />
        }
      />
    </Routes>
  );
}

export default App;