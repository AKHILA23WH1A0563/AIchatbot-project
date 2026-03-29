import React, { useState, useEffect } from "react";
import "./Login.css";
import { Link, useNavigate } from "react-router-dom";
import { loadGoogleScript, initGoogleButton, isGoogleEnabled } from "./googleAuth";

const BASE_URL = process.env.REACT_APP_BASE_URL || "http://localhost:8000";

function Login() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    if (!isGoogleEnabled()) return;
    loadGoogleScript(() => initGoogleButton("google-signin-btn", handleGoogleResponse));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handleGoogleResponse = async (response) => {
    setGoogleLoading(true);
    setMessage("");
    try {
      const res = await fetch(`${BASE_URL}/auth/google`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ credential: response.credential }),
      });
      const data = await res.json();
      if (res.ok) {
        saveAndRedirect(data);
      } else {
        setMessage(data.detail || "Google sign-in failed. Please try again.");
      }
    } catch {
      setMessage("Unable to connect to the server. Please check your internet connection.");
    } finally {
      setGoogleLoading(false);
    }
  };

  const saveAndRedirect = (data) => {
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("userName", data.user.fullName);
    localStorage.setItem("userId", data.user.id || data.user.email);
    setMessage("Login successful! Redirecting...");
    setSuccess(true);
    setTimeout(() => navigate("/home"), 1000);
  };

  const handleLogin = async () => {
    setMessage("");
    setSuccess(false);

    if (!identifier || !password) {
      setMessage("Please enter your email/mobile and password.");
      return;
    }

    const isEmail = identifier.includes("@");
    const isMobile = /^\d+$/.test(identifier);

    if (isEmail) {
      if (!/^[a-zA-Z][a-zA-Z0-9._]*@gmail\.com$/.test(identifier)) {
        setMessage("Enter a valid Gmail address (e.g. abc@gmail.com).");
        return;
      }
    } else if (isMobile) {
      if (identifier.length !== 10) {
        setMessage("Mobile number must be exactly 10 digits.");
        return;
      }
    } else {
      setMessage("Enter a valid email address or 10-digit mobile number.");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identifier, password }),
      });
      const data = await response.json();
      if (response.ok) {
        saveAndRedirect(data);
      } else {
        setMessage(data.detail || "Login failed. Please check your credentials.");
      }
    } catch {
      setMessage("Unable to reach the server. Please try again later.");
    }
  };

  return (
    <div className="login-page">
      <div className="login-overlay">
        <div className="login-title">
          <h2>AI Travel Assistant</h2>
          <p>Your journey continues here ✈️</p>
        </div>
        <div className="login-form">
          <h1>Login</h1>
          <input
            type="text"
            placeholder="Email or Mobile Number"
            value={identifier}
            autoComplete="off"
            onChange={(e) => setIdentifier(e.target.value.trim())}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            autoComplete="new-password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin}>Login</button>
          <div className="forgot-password">Forgot Password?</div>

          {isGoogleEnabled() && (
            <>
              <div className="divider">— or —</div>
              {googleLoading
                ? <p style={{ textAlign: "center", color: "#666" }}>Signing in with Google...</p>
                : <div id="google-signin-btn"></div>
              }
            </>
          )}

          <p className="register-text">
            Don't have an account?{" "}
            <Link to="/register" className="register-link">Register</Link>
          </p>
          {message && <p className={success ? "success-msg" : "error-msg"}>{message}</p>}
        </div>
      </div>
    </div>
  );
}

export default Login;
