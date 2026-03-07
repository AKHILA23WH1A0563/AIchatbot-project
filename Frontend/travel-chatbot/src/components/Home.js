import React, { useState } from "react";
import "./Home.css";

function Home() {
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you with your travel plans today?", sender: "ai" }
  ]);

  const handleSend = async () => {
    if (question.trim() !== "") {

      const userMessage = { text: question, sender: "user" };
      setMessages((prev) => [...prev, userMessage]);

      const currentQuestion = question;
      setQuestion("");

      try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message: currentQuestion })
        });

        const data = await response.json();

        setMessages((prev) => [
          ...prev,
          { text: data.reply, sender: "ai" }
        ]);

      } catch (error) {
        console.error("Error communicating with backend:", error);

        setMessages((prev) => [
          ...prev,
          { text: "Error: Could not connect to the server.", sender: "ai" }
        ]);
      }
    }
  };

  const handleNewChat = () => {
    setMessages([
      { text: "New Chat Started! How can I help?", sender: "ai" }
    ]);
    setQuestion("");
  };

  return (
    <div className="home-page">

      <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
      </style>

      {/* HEADER */}
      <div className="home-header">
        <button className="new-chat-btn" onClick={handleNewChat}>
          <span>+</span> New Chat
        </button>

        <div className="menu-dropdown">
          <div className="menu-item">🕒 Chat History</div>
          <div className="menu-item">☀ Light Theme</div>
        </div>
      </div>

      {/* MAIN */}
      <div className="home-main">

        {messages.length <= 1 ? (

          <div className="hero-text">
            <h1>Make Your Travel <br /> Easy</h1>
            <p>Your personal AI assistant for planning and exploration.</p>
          </div>

        ) : (

          <div className="chat-window">

            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message-bubble ${msg.sender}-bubble`}
                style={{ whiteSpace: "pre-line" }}
              >
                {msg.text
                  .replace(/\s+/g, " ")
                  .replace(/(\d+\.)/g, "\n$1")}
              </div>
            ))}

          </div>

        )}

      </div>

      {/* FOOTER */}
      <div className="home-footer">
        <div className="search-container">

          <input
            type="text"
            placeholder="Ask your travel question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />

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