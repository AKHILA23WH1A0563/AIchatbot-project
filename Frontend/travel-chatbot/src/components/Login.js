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

    // ---------- EMPTY CHECK ----------
    if (!identifier || !password) {
      setMessage("All fields are required");
      return;
    }

    const isEmail = identifier.includes("@");
    const isMobile = /^\d+$/.test(identifier);

    // ---------- VALIDATION ----------
    if (isEmail) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(identifier)) {
        setMessage("Enter a valid email address");
        return;
      }
    } else if (isMobile) {
      if (identifier.length !== 10) {
        setMessage("Mobile number must contain exactly 10 digits");
        return;
      }
    } else {
      setMessage("Enter a valid Email or Mobile Number");
      return;
    }

    // ---------- BACKEND CALL ----------
    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          identifier: identifier,
          password: password
        })
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Login successful! Redirecting...");
        setSuccess(true);

        // Save user name if exists
        if (data.user && data.user.fullName) {
          localStorage.setItem("userName", data.user.fullName);
        }

        setTimeout(() => {
          navigate("/home");
        }, 1000);

      } else {
        // 🔥 HANDLE FASTAPI VALIDATION ERRORS
        if (data.detail) {
          if (Array.isArray(data.detail)) {
            // If backend returns list of errors
            const errorMessages = data.detail.map(err => err.msg);
            setMessage(errorMessages.join(", "));
          } else {
            // If backend returns single string
            setMessage(data.detail);
          }
        } else {
          setMessage("Login failed. Check your credentials.");
        }
      }

    } catch (error) {
      console.error("Login Error:", error);
      setMessage("Cannot reach the server. Is Python running on port 8000?");
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