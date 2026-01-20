import React, { useState } from "react";
import "./Register.css";
import { Link } from "react-router-dom";

function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const handleRegister = () => {
    setMessage("");
    setSuccess(false);

    if (!fullName || !email || !password || !confirmPassword) {
      setMessage("Please fill all mandatory fields");
      return;
    }

    const emailRegex = /^[a-zA-Z][a-zA-Z0-9._]*@gmail\.com$/;
    if (!emailRegex.test(email)) {
      setMessage("Enter a valid email address");
      return;
    }

    if (mobile && !/^\d{10}$/.test(mobile)) {
      setMessage("Mobile number must contain exactly 10 digits");
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Password and Confirm Password must match");
      return;
    }

    setMessage("Registration successful");
    setSuccess(true);

    setFullName("");
    setEmail("");
    setMobile("");
    setPassword("");
    setConfirmPassword("");
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
          <label>
            Full Name <span className="required">*</span>
          </label>
          <input
            type="text"
            placeholder="Enter full name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </div>

        <div className="field">
          <label>
            Email <span className="required">*</span>
          </label>
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
          <label>
            Password <span className="required">*</span>
          </label>
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <div className="field">
          <label>
            Confirm Password <span className="required">*</span>
          </label>
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
          <Link to="/login" className="login-link-text">
            Login
          </Link>
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
