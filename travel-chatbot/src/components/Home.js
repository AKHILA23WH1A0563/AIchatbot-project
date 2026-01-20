import React, { useState } from "react";
import "./Home.css";

function Home() {
  const [question, setQuestion] = useState("");

  const handleSend = () => {
    if (question.trim() !== "") {
      alert(`Sending: ${question}`);
      setQuestion(""); 
    }
  };

  const handleNewChat = () => {
    setQuestion("");
    alert("New Chat Started");
  };

  return (
    <div className="home-page">
      {/* Google Font Import for beautiful typography */}
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
      </style>

      <div className="home-header">
        <button className="new-chat-btn" onClick={handleNewChat}>
          <span>+</span> New Chat
        </button>
        
        <div className="menu-dropdown">
          <div className="menu-item">🕒 Chat History</div>
          <div className="menu-item">☀ Light Theme</div>
        </div>
      </div>

      <div className="home-main">
        <h1>Make Your Travel <br /> Easy</h1>
        <p>Your personal AI assistant for planning and exploration.</p>
      </div>

      <div className="home-footer">
        <div className="search-container">
          <input
            type="text"
            placeholder="Ask your travel question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          {/* Static class ensures it is always blue */}
          <button className="send-icon-btn" onClick={handleSend}>
            ➤
          </button>
        </div>
      </div>
      
      <div className="sparkle">✦</div>
    </div>
  );
}

export default Home;