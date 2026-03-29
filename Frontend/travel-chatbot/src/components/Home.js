import React, { useState, useEffect, useRef } from "react";
import "./Home.css";
import DeleteModal from "./DeleteModal";

// Centralized API URL for your EC2 Backend
const BASE_URL = "http://13.205.31.186:8000";

function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you with your travel plans today?", sender: "ai" }
  ]);
  const [isDarkTheme, setIsDarkTheme] = useState(true);
  const [showHistory, setShowHistory] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  const [userId] = useState(
    localStorage.getItem("userId") ||
      "user_" + Math.random().toString(36).substr(2, 9)
  );

  const [sessions, setSessions] = useState([]);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [sessionToDelete, setSessionToDelete] = useState(null);

  const chatWindowRef = useRef(null);

  useEffect(() => {
    localStorage.setItem("userId", userId);
  }, [userId]);

  useEffect(() => {
    loadSessions();
    restoreLastSession();
  }, [userId]); // eslint-disable-line react-hooks/exhaustive-deps

  const restoreLastSession = async () => {
    const lastSessionId = localStorage.getItem("lastSessionId");
    if (!lastSessionId) return;

    try {
      // UPDATED: Pointing to EC2 Public IP
      const response = await fetch(`${BASE_URL}/chat/history/${lastSessionId}`);
      const data = await response.json();

      if (data.messages && data.messages.length > 0) {
        const loadedMessages = data.messages
          .map((msg) => [
            { text: msg.query, sender: "user" },
            { text: msg.response, sender: "ai" }
          ])
          .flat();

        setMessages(loadedMessages);
        setSessionId(lastSessionId);
      }
    } catch (error) {
      console.error("Error restoring session:", error);
    }
  };

  const loadSessions = async () => {
    try {
      // UPDATED: Pointing to EC2 Public IP
      const response = await fetch(`${BASE_URL}/chat/sessions/${userId}`);
      const data = await response.json();
      setSessions(data.sessions || []);
    } catch (error) {
      console.error("Error loading sessions:", error);
    }
  };

  const loadSessionHistory = async (session_id) => {
    try {
      // UPDATED: Pointing to EC2 Public IP
      const response = await fetch(`${BASE_URL}/chat/history/${session_id}`);
      const data = await response.json();

      if (data.messages && data.messages.length > 0) {
        const loadedMessages = data.messages
          .map((msg) => [
            { text: msg.query, sender: "user" },
            { text: msg.response, sender: "ai" }
          ])
          .flat();

        setMessages(loadedMessages);
        setSessionId(session_id);
        localStorage.setItem("lastSessionId", session_id);
      }
    } catch (error) {
      console.error("Error loading history:", error);
    }
  };

  const deleteSession = async (session_id) => {
    setSessionToDelete(session_id);
    setShowDeleteModal(true);
  };

  const confirmDelete = async () => {
    if (!sessionToDelete) return;

    try {
      const token = localStorage.getItem("token");

      // UPDATED: Pointing to EC2 Public IP via /api/v1 prefix
      const response = await fetch(
        `${BASE_URL}/api/v1/sessions/sessions/${sessionToDelete}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      if (response.ok) {
        loadSessions();

        if (sessionId === sessionToDelete) {
          localStorage.removeItem("lastSessionId");
          handleNewChat();
        }
      } else {
        console.log("Delete failed:", response.status);
      }
    } catch (error) {
      console.error("Error deleting session:", error);
    }

    setShowDeleteModal(false);
    setSessionToDelete(null);
  };

  const cancelDelete = () => {
    setShowDeleteModal(false);
    setSessionToDelete(null);
  };

  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  const formatMessage = (text) => {
    if (!text) return "";
    const lines = text.split("\n");
    return lines.map((line, index) => {
      const processedLine = line.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

      if (/^\d+\.\s/.test(line)) {
        return (
          <div key={index} className="list-item numbered" dangerouslySetInnerHTML={{ __html: processedLine }} />
        );
      } else if (/^[-•*+]\s/.test(line)) {
        return (
          <div key={index} className="list-item bullet" dangerouslySetInnerHTML={{ __html: processedLine }} />
        );
      } else if (/^\*\*.*\*\*:?$/.test(line) || (line === line.toUpperCase() && line.length > 3 && line.length < 50)) {
        return (
          <div key={index} className="message-heading" dangerouslySetInnerHTML={{ __html: processedLine }} />
        );
      } else if (line.trim()) {
        return (
          <div key={index} className="message-line" dangerouslySetInnerHTML={{ __html: processedLine }} />
        );
      } else {
        return <div key={index} className="message-spacer"></div>;
      }
    });
  };

  const handleSend = async () => {
    if (question.trim() === "") return;

    const userMessage = { text: question, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);

    const currentQuestion = question;
    setQuestion("");

    try {
      // UPDATED: Pointing to EC2 Public IP
      const response = await fetch(`${BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: currentQuestion,
          session_id: sessionId,
          user_id: userId
        })
      });

      const data = await response.json();

      if (data.session_id) {
        setSessionId(data.session_id);
        localStorage.setItem("lastSessionId", data.session_id);
      }

      setMessages((prev) => [...prev, { text: data.reply, sender: "ai" }]);
      loadSessions();
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { text: "Error connecting to server. Ensure EC2 Port 8000 is open.", sender: "ai" }
      ]);
    }
  };

  const handleNewChat = () => {
    setMessages([{ text: "New Chat Started! How can I help?", sender: "ai" }]);
    setQuestion("");
    setSessionId(null);
    localStorage.removeItem("lastSessionId");
    loadSessions();
  };

  const toggleTheme = () => setIsDarkTheme(!isDarkTheme);
  const toggleHistory = () => setShowHistory(!showHistory);

  const handleSignOut = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
    localStorage.removeItem("lastSessionId");
    window.location.href = "/login";
  };

  return (
    <div className={`home-page ${isDarkTheme ? "dark-theme" : "light-theme"}`}>
      <div className="sidebar">
        <button className="menu-btn" onClick={handleNewChat}>+ New Chat</button>
        <button className="menu-btn" onClick={toggleHistory}>🕒 Chat History</button>
        <button className="menu-btn" onClick={toggleTheme}>
          {isDarkTheme ? "☀️ Light Theme" : "🌙 Dark Theme"}
        </button>

        {showHistory && (
          <div className="history-panel">
            <h3>Chat Sessions</h3>
            {sessions.length > 0 ? (
              <div className="session-list">
                {sessions.map((session, index) => (
                  <div key={index} className="session-item">
                    <div className="session-preview" onClick={() => loadSessionHistory(session.session_id)} style={{ cursor: "pointer" }}>
                      {session.preview}
                    </div>
                    <div className="session-meta">{session.message_count} messages</div>
                    <button className="delete-btn" onClick={() => deleteSession(session.session_id)}>Delete</button>
                  </div>
                ))}
              </div>
            ) : (<p>No previous chats</p>)}
          </div>
        )}
        <button className="menu-btn signout-btn" onClick={handleSignOut}>Sign Out</button>
      </div>

      <div className="main-content">
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
                  {msg.sender === "ai" ? formatMessage(msg.text) : msg.text}
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
            <button className="send-icon-btn" onClick={handleSend}>➤</button>
          </div>
        </div>
        <div className="sparkle">✦</div>
      </div>

      <DeleteModal isOpen={showDeleteModal} onClose={cancelDelete} onConfirm={confirmDelete} />
    </div>
  );
}

export default Home;