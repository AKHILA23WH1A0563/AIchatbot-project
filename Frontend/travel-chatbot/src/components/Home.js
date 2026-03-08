import React, { useState, useEffect, useRef } from "react";
import "./Home.css";

function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you with your travel plans today?", sender: "ai" }
  ]);
  const [isDarkTheme, setIsDarkTheme] = useState(true);
  const [showHistory, setShowHistory] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [userId] = useState(localStorage.getItem("userId") || "user_" + Math.random().toString(36).substr(2, 9));
  const [sessions, setSessions] = useState([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const chatWindowRef = useRef(null);

  // Save userId to localStorage
  useEffect(() => {
    localStorage.setItem("userId", userId);
  }, [userId]);

  // Load sessions and restore last session on mount
  useEffect(() => {
    loadSessions();
    restoreLastSession();
  }, [userId]);

  const restoreLastSession = async () => {
    const lastSessionId = localStorage.getItem("lastSessionId");
    if (lastSessionId) {
      setIsLoadingHistory(true);
      try {
        const response = await fetch(`http://127.0.0.1:8000/chat/history/${lastSessionId}`);
        const data = await response.json();
        
        if (data.messages && data.messages.length > 0) {
          const loadedMessages = data.messages.map(msg => ([
            { text: msg.query, sender: "user" },
            { text: msg.response, sender: "ai" }
          ])).flat();
          
          setMessages(loadedMessages);
          setSessionId(lastSessionId);
        }
      } catch (error) {
        console.error("Error restoring session:", error);
      }
      setIsLoadingHistory(false);
    }
  };

  const loadSessions = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/chat/sessions/${userId}`);
      const data = await response.json();
      setSessions(data.sessions || []);
    } catch (error) {
      console.error("Error loading sessions:", error);
    }
  };

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  // Format message text with proper line breaks and lists
  const formatMessage = (text) => {
    if (!text) return "";
    
    const lines = text.split('\n');
    
    return lines.map((line, index) => {
      const processedLine = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      if (/^\d+\.\s/.test(line)) {
        return (
          <div key={index} className="list-item numbered" dangerouslySetInnerHTML={{ __html: processedLine }} />
        );
      }
      else if (/^[-•*]\s/.test(line)) {
        return (
          <div key={index} className="list-item bullet" dangerouslySetInnerHTML={{ __html: processedLine }} />
        );
      }
      else if (/^\*\*.*\*\*:?$/.test(line) || (line === line.toUpperCase() && line.length > 3 && line.length < 50)) {
        return (
          <div key={index} className="message-heading" dangerouslySetInnerHTML={{ __html: processedLine }} />
        );
      }
      else if (line.trim()) {
        return (
          <div key={index} className="message-line" dangerouslySetInnerHTML={{ __html: processedLine }} />
        );
      }
      else {
        return <div key={index} className="message-spacer"></div>;
      }
    });
  };

  const handleSend = async () => {
    if (question.trim() !== "") {
      const userMessage = { text: question, sender: "user" };
      setMessages((prev) => [...prev, userMessage]);
      
      const currentQuestion = question;
      setQuestion("");

      try {
        const response = await fetch('http://127.0.0.1:8000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            message: currentQuestion,
            session_id: sessionId,
            user_id: userId
          }),
        });

        const data = await response.json();
        
        // Save session_id from response
        if (data.session_id) {
          setSessionId(data.session_id);
          localStorage.setItem("lastSessionId", data.session_id);
        }
        
        setMessages((prev) => [...prev, { text: data.reply, sender: "ai" }]);
      } catch (error) {
        console.error("Error communicating with backend:", error);
        setMessages((prev) => [...prev, { text: "Error: Could not connect to the server.", sender: "ai" }]);
      }
    }
  };

  const handleNewChat = () => {
    setMessages([{ text: "New Chat Started! How can I help?", sender: "ai" }]);
    setQuestion("");
    setSessionId(null);
    localStorage.removeItem("lastSessionId");
    loadSessions();
  };

  const toggleTheme = () => {
    setIsDarkTheme(!isDarkTheme);
  };

  const toggleHistory = () => {
    setShowHistory(!showHistory);
  };

  return (
    <div className={`home-page ${isDarkTheme ? 'dark-theme' : 'light-theme'}`}>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
      </style>

      <div className="home-header">
        <button className="new-chat-btn" onClick={handleNewChat}>
          <span>+</span> New Chat
        </button>
        
        <div className="menu-dropdown">
          <div className="menu-item" onClick={toggleHistory}>
            🕒 Chat History
          </div>
          <div className="menu-item" onClick={toggleTheme}>
            {isDarkTheme ? '☀️ Light Theme' : '🌙 Dark Theme'}
          </div>
        </div>
      </div>

      {showHistory && (
        <div className="history-panel">
          <h3>Chat Sessions</h3>
          {sessions.length > 0 ? (
            <div className="session-list">
              {sessions.map((session, index) => (
                <div key={index} className="session-item">
                  <div className="session-preview">{session.preview}</div>
                  <div className="session-meta">
                    {session.message_count} messages
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No previous chats</p>
          )}
        </div>
      )}

      <div className="home-main">
        {messages.length <= 1 ? (
          <>
            <h1>Make Your Travel <br /> Easy</h1>
            <p>Your personal AI assistant for planning and exploration.</p>
          </>
        ) : (
          <div className="chat-window" ref={chatWindowRef}>
            {messages.map((msg, index) => (
              <div key={index} className={`message-bubble ${msg.sender}-bubble`}>
                {msg.sender === 'ai' ? formatMessage(msg.text) : msg.text}
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