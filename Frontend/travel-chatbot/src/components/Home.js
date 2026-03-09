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

  const [userId] = useState(
    localStorage.getItem("userId") ||
    "user_" + Math.random().toString(36).substr(2, 9)
  );

  const [sessions, setSessions] = useState([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  const chatWindowRef = useRef(null);

  // Save userId
  useEffect(() => {
    localStorage.setItem("userId", userId);
  }, [userId]);

  // Load sessions + restore last chat
  useEffect(() => {
    loadSessions();
    restoreLastSession();
  }, [userId]);

  // Restore previous session
  const restoreLastSession = async () => {

    const lastSessionId = localStorage.getItem("lastSessionId");

    if (!lastSessionId) return;

    setIsLoadingHistory(true);

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/chat/history/${lastSessionId}`
      );

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
  };

  // Load sessions list
  const loadSessions = async () => {

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/chat/sessions/${userId}`
      );

      const data = await response.json();

      setSessions(data.sessions || []);

    } catch (error) {
      console.error("Error loading sessions:", error);
    }
  };

  // Load previous chat
  const loadSessionHistory = async (session_id) => {

    try {

      setIsLoadingHistory(true);

      const response = await fetch(
        `http://127.0.0.1:8000/chat/history/${session_id}`
      );

      const data = await response.json();

      if (data.messages && data.messages.length > 0) {

        const loadedMessages = data.messages.map(msg => ([
          { text: msg.query, sender: "user" },
          { text: msg.response, sender: "ai" }
        ])).flat();

        setMessages(loadedMessages);
        setSessionId(session_id);

        localStorage.setItem("lastSessionId", session_id);
      }

    } catch (error) {
      console.error("Error loading history:", error);
    }

    setIsLoadingHistory(false);
  };

  // Delete session
  const deleteSession = async (session_id) => {

  if (!window.confirm("Delete this chat session?")) return;

  try {

    const token = localStorage.getItem("token");   // get token from login

    const response = await fetch(
      `http://127.0.0.1:8000/api/v1/sessions/sessions/${session_id}`,
      {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      }
    );

    if (response.ok) {

      alert("Session deleted");

      loadSessions();

      if (sessionId === session_id) {
        localStorage.removeItem("lastSessionId");
        handleNewChat();
      }

    } else {

      console.log("Delete failed:", response.status);

    }

  } catch (error) {

    console.error("Error deleting session:", error);

  }

};

  // Auto scroll chat
  useEffect(() => {

    if (chatWindowRef.current) {

      chatWindowRef.current.scrollTop =
        chatWindowRef.current.scrollHeight;

    }

  }, [messages]);

  // Format AI messages
  const formatMessage = (text) => {

    if (!text) return "";

    const lines = text.split("\n");

    return lines.map((line, index) => {

      const processedLine = line.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
      );

      if (/^\d+\.\s/.test(line)) {

        return (
          <div
            key={index}
            className="list-item numbered"
            dangerouslySetInnerHTML={{ __html: processedLine }}
          />
        );

      }

      else if (/^[-•*]\s/.test(line)) {

        return (
          <div
            key={index}
            className="list-item bullet"
            dangerouslySetInnerHTML={{ __html: processedLine }}
          />
        );

      }

      else if (
        /^\*\*.*\*\*:?$/.test(line) ||
        (line === line.toUpperCase() &&
          line.length > 3 &&
          line.length < 50)
      ) {

        return (
          <div
            key={index}
            className="message-heading"
            dangerouslySetInnerHTML={{ __html: processedLine }}
          />
        );

      }

      else if (line.trim()) {

        return (
          <div
            key={index}
            className="message-line"
            dangerouslySetInnerHTML={{ __html: processedLine }}
          />
        );

      }

      else {

        return <div key={index} className="message-spacer"></div>;

      }

    });

  };

  // Send message
  const handleSend = async () => {

    if (question.trim() === "") return;

    const userMessage = { text: question, sender: "user" };

    setMessages(prev => [...prev, userMessage]);

    const currentQuestion = question;

    setQuestion("");

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: currentQuestion,
            session_id: sessionId,
            user_id: userId
          })
        }
      );

      const data = await response.json();

      if (data.session_id) {

        setSessionId(data.session_id);

        localStorage.setItem("lastSessionId", data.session_id);

      }

      setMessages(prev => [
        ...prev,
        { text: data.reply, sender: "ai" }
      ]);

      loadSessions();

    } catch (error) {

      console.error(error);

      setMessages(prev => [
        ...prev,
        { text: "Error connecting to server.", sender: "ai" }
      ]);

    }

  };

  // Start new chat
  const handleNewChat = () => {

    setMessages([
      { text: "New Chat Started! How can I help?", sender: "ai" }
    ]);

    setQuestion("");

    setSessionId(null);

    localStorage.removeItem("lastSessionId");

    loadSessions();
  };

  const toggleTheme = () => setIsDarkTheme(!isDarkTheme);

  const toggleHistory = () => setShowHistory(!showHistory);

  return (

    <div className={`home-page ${isDarkTheme ? "dark-theme" : "light-theme"}`}>

      <div className="home-header">

        <button className="new-chat-btn" onClick={handleNewChat}>
          + New Chat
        </button>

        <div className="menu-dropdown">

          <div className="menu-item" onClick={toggleHistory}>
            🕒 Chat History
          </div>

          <div className="menu-item" onClick={toggleTheme}>
            {isDarkTheme ? "☀️ Light Theme" : "🌙 Dark Theme"}
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

                  <div
                    className="session-preview"
                    onClick={() =>
                      loadSessionHistory(session.session_id)
                    }
                    style={{ cursor: "pointer" }}
                  >
                    {session.preview}
                  </div>

                  <div className="session-meta">
                    {session.message_count} messages
                  </div>

                  <button
                    onClick={() =>
                      deleteSession(session.session_id)
                    }
                    style={{
                      marginTop: "5px",
                      color: "red",
                      border: "none",
                      background: "transparent",
                      cursor: "pointer"
                    }}
                  >
                    Delete
                  </button>

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

              <div
                key={index}
                className={`message-bubble ${msg.sender}-bubble`}
              >

                {msg.sender === "ai"
                  ? formatMessage(msg.text)
                  : msg.text}

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