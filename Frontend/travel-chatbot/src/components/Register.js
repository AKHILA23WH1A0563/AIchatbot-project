import React, { useState, useEffect } from "react";
import "./Register.css";
import { Link, useNavigate } from "react-router-dom";
import { loadGoogleScript, initGoogleButton, isGoogleEnabled } from "./googleAuth";

const BASE_URL = process.env.REACT_APP_BASE_URL || "http://localhost:8000";

const passwordRules = [
  { label: "At least 8 characters", test: (p) => p.length >= 8 },
  { label: "One uppercase letter", test: (p) => /[A-Z]/.test(p) },
  { label: "One lowercase letter", test: (p) => /[a-z]/.test(p) },
  { label: "One number", test: (p) => /\d/.test(p) },
  { label: "One special character (!@#$...)", test: (p) => /[!@#$%^&*(),.?":{}|<>]/.test(p) },
];

function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);

  const navigate = useNavigate();

  const passedRules = passwordRules.filter((r) => r.test(password));
  const strength = passedRules.length;
  const strengthLabel = ["", "Weak", "Weak", "Fair", "Good", "Strong"][strength];
  const strengthColor = ["", "#e74c3c", "#e74c3c", "#f39c12", "#2ecc71", "#27ae60"][strength];

  useEffect(() => {
    if (!isGoogleEnabled()) return;
    loadGoogleScript(() => initGoogleButton("google-signup-btn", handleGoogleResponse));
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
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("userName", data.user.fullName);
        localStorage.setItem("userId", data.user.id || data.user.email);
        setMessage("Google sign-up successful! Redirecting...");
        setSuccess(true);
        setTimeout(() => navigate("/home"), 1000);
      } else {
        setMessage(data.detail || "Google sign-up failed. Please try again.");
      }
    } catch {
      setMessage("Unable to connect to the server. Please check your internet connection.");
    } finally {
      setGoogleLoading(false);
    }
  };

  const handleRegister = async () => {
    setMessage("");
    setSuccess(false);

    if (!fullName || !email || !password || !confirmPassword) {
      setMessage("Please fill all mandatory fields.");
      return;
    }

    if (!/^[a-zA-Z][a-zA-Z0-9._]*@gmail\.com$/.test(email)) {
      setMessage("Enter a valid Gmail address (e.g. abc@gmail.com).");
      return;
    }

    if (strength < 5) {
      setMessage("Password does not meet all requirements.");
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Passwords do not match.");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fullName, email, mobileNumber: mobile, password, confirmPassword }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Account created successfully! Redirecting to login...");
        setSuccess(true);
        setFullName(""); setEmail(""); setMobile(""); setPassword(""); setConfirmPassword("");
        setTimeout(() => navigate("/login"), 2000);
      } else {
        setMessage(data.detail || "Registration failed. Please try again.");
      }
    } catch {
      setMessage("Unable to reach the server. Please try again later.");
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

        {isGoogleEnabled() && (
          <>
            {googleLoading
              ? <p style={{ textAlign: "center", color: "#666" }}>Signing up with Google...</p>
              : <div id="google-signup-btn"></div>
            }
            <div className="divider">— or sign up with email —</div>
          </>
        )}

        <div className="field">
          <label>Full Name <span className="required">*</span></label>
          <input type="text" placeholder="Enter full name" value={fullName} onChange={(e) => setFullName(e.target.value)} />
        </div>

        <div className="field">
          <label>Email <span className="required">*</span></label>
          <input type="email" placeholder="Enter email" value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>

        <div className="field">
          <label>Mobile Number</label>
          <input type="text" placeholder="10-digit mobile number (optional)" value={mobile} onChange={(e) => setMobile(e.target.value.replace(/\D/g, ""))} />
        </div>

        <div className="field">
          <label>Password <span className="required">*</span></label>
          <input type="password" placeholder="Enter password" value={password} onChange={(e) => setPassword(e.target.value)} />
          {password && (
            <div className="password-strength">
              <div className="strength-bar">
                {[1,2,3,4,5].map((i) => (
                  <div key={i} className="strength-segment" style={{ background: i <= strength ? strengthColor : "#444" }} />
                ))}
              </div>
              <span style={{ color: strengthColor, fontSize: "12px" }}>{strengthLabel}</span>
              <ul className="password-rules">
                {passwordRules.map((rule, i) => (
                  <li key={i} style={{ color: rule.test(password) ? "#2ecc71" : "#e74c3c" }}>
                    {rule.test(password) ? "✓" : "✗"} {rule.label}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="field">
          <label>Confirm Password <span className="required">*</span></label>
          <input type="password" placeholder="Re-enter password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
        </div>

        <button onClick={handleRegister}>Register</button>

        <p className="login-link">
          Already have an account?{" "}
          <Link to="/login" className="login-link-text">Login</Link>
        </p>

        {message && <p className={success ? "success-msg" : "error-msg"}>{message}</p>}
      </div>
    </div>
  );
}

export default Register;
