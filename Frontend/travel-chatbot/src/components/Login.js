import React, { useState } from "react";
import "./Login.css";
import { Link, useNavigate } from "react-router-dom";

function Login() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const navigate = useNavigate();

  const handleLogin = async () => {
    setMessage("");
    setSuccess(false);

    if (!identifier || !password) {
      setMessage("All fields are required");
      return;
    }

    /* ✅ UNIVERSAL EMAIL VALIDATION */
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(identifier)) {
      setMessage("Enter a valid email address");
      return;
    }

    /* ---------- BACKEND INTEGRATION ---------- */
    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: identifier,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Login successful! Redirecting...");
        setSuccess(true);

        localStorage.setItem("userName", data.full_name);

        setTimeout(() => {
          navigate("/home");
        }, 1000);
      } else {
        setMessage(data.detail || "Login failed. Check your credentials.");
      }
    } catch (error) {
      console.error("Login Error:", error);
      setMessage("Cannot reach the server. Is Python running?");
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
            placeholder="Email"
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

          <p className="register-text">
            Don’t have an account?{" "}
            <Link to="/register" className="register-link">
              Register
            </Link>
          </p>

          {message && (
            <p className={success ? "success-msg" : "error-msg"}>
              {message}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Login;