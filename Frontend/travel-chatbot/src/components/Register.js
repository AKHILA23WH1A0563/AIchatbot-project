import React, { useState } from "react";
import "./Register.css";
import { Link, useNavigate } from "react-router-dom"; // Added useNavigate for redirection

function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);
  
  const navigate = useNavigate(); // Hook to change pages after success

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

    // 2. Integration Logic (Connecting to Python Backend)
    try {
      const response = await fetch('http://127.0.0.1:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          full_name: fullName,
          email: email,
          mobile: mobile,
          password: password
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

        // Move to login page after 2 seconds
        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else {
        // Show the error message from the Python Backend
        setMessage(data.detail || "Registration failed");
      }
    } catch (error) {
      console.error("Connection Error:", error);
      setMessage("Backend server not reached. Check if Python is running on port 8000.");
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