import React, { useState } from "react";
import "./Login.css";
import { Link } from "react-router-dom";

function Login() {
  const [identifier, setIdentifier] = useState(""); // email OR mobile
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const handleLogin = () => {
    setMessage("");
    setSuccess(false);

    if (!identifier || !password) {
      setMessage("All fields are required");
      return;
    }

    const isEmail = identifier.includes("@");
    const isMobile = /^\d+$/.test(identifier);

    /* ---------- EMAIL VALIDATION ---------- */
    if (isEmail) {
      if (!/^[a-zA-Z]/.test(identifier)) {
        setMessage("Email must start with alphabets");
        return;
      }

      const emailRegex = /^[a-zA-Z][a-zA-Z0-9._]*@gmail\.com$/;

      if (!emailRegex.test(identifier)) {
        setMessage("Enter email in valid format (example: abc@gmail.com)");
        return;
      }
    }

    /* ---------- MOBILE VALIDATION ---------- */
    else if (isMobile) {
      if (identifier.length !== 10) {
        setMessage("Mobile number must contain exactly 10 digits");
        return;
      }
    }

    /* ---------- INVALID INPUT ---------- */
    else {
      setMessage("Enter a valid Email or Mobile Number");
      return;
    }

    /* ---------- SUCCESS ---------- */
    setMessage("Login successful");
    setSuccess(true);

    setIdentifier("");
    setPassword("");
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