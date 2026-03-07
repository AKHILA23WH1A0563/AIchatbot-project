import React, { useState } from "react";
import "./Login.css";
import { Link, useNavigate } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const navigate = useNavigate();

  const handleLogin = async () => {
    setMessage("");
    setSuccess(false);

    if (!email || !password) {
      setMessage("All fields are required");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          identifier: email, // matches backend
          password
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
        setMessage("Login successful! Redirecting...");
        localStorage.setItem("userName", data.user.full_name || "");
        localStorage.setItem("userEmail", data.user.email || "");

        setTimeout(() => navigate("/home"), 1000);
      } else {
        if (Array.isArray(data.detail)) {
          setMessage(data.detail.map(err => err.msg || err.message).join(", "));
        } else if (typeof data.detail === "string") {
          setMessage(data.detail);
        } else {
          setMessage("Login failed. Please try again.");
        }
      }
    } catch (error) {
      console.error("Login Error:", error);
      setMessage("Cannot connect to server (Port 8000).");
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

          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
          <button onClick={handleLogin} onKeyDown={(e) => e.key === "Enter" && handleLogin()}>
            Login
          </button>

          <p>
            Don’t have an account? <Link to="/register">Register</Link>
          </p>

          {message && <p className={success ? "success-msg" : "error-msg"}>{message}</p>}
        </div>
      </div>
    </div>
  );
}

export default Login;