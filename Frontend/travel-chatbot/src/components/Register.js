import React, { useState } from "react";
import "./Register.css";
import { Link, useNavigate } from "react-router-dom";

// Centralized API URL for your EC2 Backend
const BASE_URL = "http://13.205.31.186:8000";

function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);
  
  const navigate = useNavigate();

  const handleRegister = async () => {
    setMessage("");
    setSuccess(false);

    // 1. Validation Logic
    if (!fullName || !email || !password || !confirmPassword) {
      setMessage("Please fill all mandatory fields");
      return;
    }

    const emailRegex = /^[a-zA-Z][a-zA-Z0-9._]*@gmail\.com$/;
    if (!emailRegex.test(email)) {
      setMessage("Enter a valid email address");
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Password and Confirm Password must match");
      return;
    }

    // 2. Integration Logic (Connecting to EC2 Backend)
    try {
      // UPDATED: Pointing to EC2 Public IP
      const response = await fetch(`${BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fullName: fullName,
          email: email,
          mobileNumber: mobile,
          password: password,
          confirmPassword: confirmPassword
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Registration successful! Redirecting to login...");
        setSuccess(true);
        
        // Clear fields
        setFullName("");
        setEmail("");
        setMobile("");
        setPassword("");
        setConfirmPassword("");

        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else {
        setMessage(data.detail || "Registration failed");
      }
    } catch (error) {
      console.error("Connection Error:", error);
      setMessage("Backend server not reached. Check if EC2 is running and Port 8000 is open.");
    }
  };

  return (
    <div className="register-page">
      <div className="form-title">
        <h2>AI Travel Assistant</h2>
        <p>Smart journeys start here ✈️</p>
      </div>

      <div className="register-form">
        <h1>Create Account</h1>

        <div className="field">
          <label>Full Name <span className="required">*</span></label>
          <input
            type="text"
            placeholder="Enter full name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </div>

        <div className="field">
          <label>Email <span className="required">*</span></label>
          <input
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="field">
          <label>Mobile Number</label>
          <input
            type="text"
            placeholder="10-digit mobile number (optional)"
            value={mobile}
            onChange={(e) => setMobile(e.target.value.replace(/\D/g, ""))}
          />
        </div>

        <div className="field">
          <label>Password <span className="required">*</span></label>
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <div className="field">
          <label>Confirm Password <span className="required">*</span></label>
          <input
            type="password"
            placeholder="Re-enter password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>

        <button onClick={handleRegister}>Register</button>

        <p className="login-link">
          Already have an account?{" "}
          <Link to="/login" className="login-link-text">Login</Link>
        </p>

        {message && (
          <p className={success ? "success-msg" : "error-msg"}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
}

export default Register;