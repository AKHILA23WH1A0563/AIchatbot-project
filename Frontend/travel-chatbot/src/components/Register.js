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
  const [step, setStep] = useState(1);
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const navigate = useNavigate();

  // --------------------------
  // Step 1: Register and generate OTP
  // --------------------------
  const handleRegister = async () => {
    setMessage("");
    setSuccess(false);

    if (!fullName || !email || !password || !confirmPassword) {
      setMessage("Please fill all required fields");
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: fullName,          // matches backend
          email,
          mobile_number: mobile,        // matches backend
          password,
          confirm_password: confirmPassword
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("OTP sent! Check backend console.");
        setStep(2); // move to OTP step
        setSuccess(true);
      } else {
        if (Array.isArray(data.detail)) {
          setMessage(data.detail.map(err => err.msg || err.message).join(", "));
        } else if (typeof data.detail === "string") {
          setMessage(data.detail);
        } else {
          setMessage("Registration failed.");
        }
      }
    } catch (error) {
      console.error("Register Error:", error);
      setMessage("Cannot connect to backend server.");
    }
  };

  // --------------------------
  // Step 2: Verify OTP
  // --------------------------
  const handleVerifyOtp = async () => {
    if (!otp) {
      setMessage("Please enter the OTP");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/verify-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, otp })
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Registration complete! Redirecting to login...");
        setSuccess(true);
        setFullName("");
        setEmail("");
        setMobile("");
        setPassword("");
        setConfirmPassword("");
        setOtp("");

        setTimeout(() => navigate("/login"), 1500);
      } else {
        if (Array.isArray(data.detail)) {
          setMessage(data.detail.map(err => err.msg || err.message).join(", "));
        } else if (typeof data.detail === "string") {
          setMessage(data.detail);
        } else {
          setMessage("OTP verification failed.");
        }
      }
    } catch (error) {
      console.error("OTP Verify Error:", error);
      setMessage("Cannot connect to backend server.");
    }
  };

  return (
    <div className="register-page">
      <div className="register-form">
        <h1>Create Account</h1>

        {step === 1 && (
          <>
            <input type="text" placeholder="Full Name" value={fullName} onChange={e => setFullName(e.target.value)} />
            <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
            <input type="text" placeholder="Mobile (optional)" value={mobile} onChange={e => setMobile(e.target.value)} />
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
            <button onClick={handleRegister}>Register</button>
          </>
        )}

        {step === 2 && (
          <>
            <p>Enter the OTP sent to your email (check backend console)</p>
            <input type="text" placeholder="OTP" value={otp} onChange={e => setOtp(e.target.value)} />
            <button onClick={handleVerifyOtp}>Verify OTP</button>
          </>
        )}

        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>

        {message && <p className={success ? "success-msg" : "error-msg"}>{message}</p>}
      </div>
    </div>
  );
}

export default Register;