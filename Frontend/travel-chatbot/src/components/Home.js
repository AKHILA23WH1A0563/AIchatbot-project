import React, { useState } from "react";
import "./Home.css";

function Home() {
  const [question, setQuestion] = useState("");
  // New state to store all messages in the conversation
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you with your travel plans today?", sender: "ai" }
  ]);

  const handleSend = async () => {
    if (question.trim() !== "") {
      // 1. Capture the user's message and add it to the UI immediately
      const userMessage = { text: question, sender: "user" };
      setMessages((prev) => [...prev, userMessage]);
      
      const currentQuestion = question; // Store to send to backend
      setQuestion(""); // Clear input field

      try {
        // 2. Send request to your FastAPI Backend
        const response = await fetch('http://127.0.0.1:8000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: currentQuestion }),
        });

        const data = await response.json();
        
        // 3. Add the AI's response to the message list
        setMessages((prev) => [...prev, { text: data.reply, sender: "ai" }]);
      } catch (error) {
        console.error("Error communicating with backend:", error);
        setMessages((prev) => [...prev, { text: "Error: Could not connect to the server.", sender: "ai" }]);
      }
    }
  };

  const handleNewChat = () => {
    // Resets the chat to the initial greeting
    setMessages([{ text: "New Chat Started! How can I help?", sender: "ai" }]);
    setQuestion("");
  };

  return (
    <div className="home-page">
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

      {/* Main content changes depending on if there are messages */}
      <div className="home-main">
        {messages.length <= 1 ? (
          <>
            <h1>Make Your Travel <br /> Easy</h1>
            <p>Your personal AI assistant for planning and exploration.</p>
          </>
        ) : (
          <div className="chat-window">
            {messages.map((msg, index) => (
              <div key={index} className={`message-bubble ${msg.sender}-bubble`}>
                {msg.text}
              </div>
            ))}
          </div>
        )}
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