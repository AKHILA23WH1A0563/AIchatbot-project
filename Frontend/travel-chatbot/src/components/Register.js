import React, { useState } from "react";
import "./Register.css";
import { Link, useNavigate } from "react-router-dom";

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

    /* ---------- VALIDATION ---------- */
    if (!fullName || !email || !password || !confirmPassword) {
      setMessage("Please fill all mandatory fields");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setMessage("Enter a valid email address");
      return;
    }

    if (mobile && mobile.length !== 10) {
      setMessage("Mobile number must be exactly 10 digits");
      return;
    }

    const passwordRegex =
      /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&]).{6,}$/;

    if (!passwordRegex.test(password)) {
      setMessage(
        "Password must be at least 6 characters and include letter, number & special character"
      );
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Password and Confirm Password must match");
      return;
    }

    /* ---------- BACKEND INTEGRATION ---------- */
    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          fullName: fullName,
          email: email,
          mobileNumber: mobile,
          password: password,
          confirmPassword: confirmPassword
        })
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Registration successful! Redirecting to login...");
        setSuccess(true);

        // Clear form
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
          <label>Mobile Number (Optional)</label>
          <input
            type="text"
            placeholder="10-digit mobile number"
            value={mobile}
            onChange={(e) =>
              setMobile(e.target.value.replace(/\D/g, ""))
            }
            maxLength="10"
          />
        </div>

        <div className="field">
          <label>Password <span className="required">*</span></label>
          <input
            type="password"
            placeholder="Minimum 6 chars (letter, number & special)"
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