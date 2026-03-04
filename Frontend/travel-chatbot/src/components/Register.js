import React, { useState } from "react";
import "./Register.css";
import { Link, useNavigate } from "react-router-dom";

function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [otp, setOtp] = useState("");
  const [showOtpField, setShowOtpField] = useState(false);

  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const navigate = useNavigate();

  // ================= EMAIL VALIDATION =================
  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  // ================= PASSWORD VALIDATION =================
  const validatePassword = (password) => {
    const passwordRegex =
      /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&]).{6,}$/;
    return passwordRegex.test(password);
  };

  // ================= REGISTER FUNCTION =================
  const handleRegister = async () => {
    setMessage("");
    setSuccess(false);

    if (!fullName || !email || !mobile || !password || !confirmPassword) {
      setMessage("Please fill all mandatory fields");
      return;
    }

    if (!validateEmail(email)) {
      setMessage("Enter a valid email address");
      return;
    }

    if (mobile.length !== 10) {
      setMessage("Mobile number must be exactly 10 digits");
      return;
    }

    if (!validatePassword(password)) {
      setMessage(
        "Password must be at least 6 characters and include letter, number & special character"
      );
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Password and Confirm Password must match");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: fullName,
          email: email,
          mobile: mobile,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("OTP sent! Check backend console.");
        setSuccess(true);
        setShowOtpField(true);
      } else {
        handleBackendError(data);
      }
    } catch (error) {
      console.error("Connection Error:", error);
      setMessage("Backend server not reachable.");
    }
  };

  // ================= VERIFY OTP FUNCTION =================
  const handleVerifyOtp = async () => {
    setMessage("");
    setSuccess(false);

    if (!otp) {
      setMessage("Enter OTP");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/verify-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email,
          otp: otp,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Registration successful! Redirecting to login...");
        setSuccess(true);

        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else {
        handleBackendError(data);
      }
    } catch (error) {
      console.error("OTP Error:", error);
      setMessage("OTP verification failed.");
    }
  };

  // ================= HANDLE BACKEND ERRORS =================
  const handleBackendError = (data) => {
    if (data?.detail) {
      if (Array.isArray(data.detail)) {
        setMessage(data.detail[0].msg);
      } else {
        setMessage(data.detail);
      }
    } else {
      setMessage("Something went wrong");
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
          <label>Full Name *</label>
          <input
            type="text"
            placeholder="Enter full name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </div>

        <div className="field">
          <label>Email *</label>
          <input
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="field">
          <label>Mobile *</label>
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
          <label>Password *</label>
          <input
            type="password"
            placeholder="Minimum 6 chars (letter, number & special)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <div className="field">
          <label>Confirm Password *</label>
          <input
            type="password"
            placeholder="Re-enter password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>

        {!showOtpField ? (
          <button onClick={handleRegister}>Register</button>
        ) : (
          <>
            <div className="field">
              <label>Enter OTP *</label>
              <input
                type="text"
                placeholder="Enter 6-digit OTP"
                value={otp}
                onChange={(e) =>
                  setOtp(e.target.value.replace(/\D/g, ""))
                }
                maxLength="6"
              />
            </div>

            <button onClick={handleVerifyOtp}>Verify OTP</button>
          </>
        )}

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