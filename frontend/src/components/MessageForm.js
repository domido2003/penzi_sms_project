import React, { useState, useEffect } from "react";
import axios from "axios";

export default function MessageForm() {
  const [sender, setSender] = useState("");
  const [content, setContent] = useState("");
  const [messages, setMessages] = useState([]);
  const [serverResponse, setServerResponse] = useState("");
  const [nextStepGuide, setNextStepGuide] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const initialize = async () => {
      await fetchMessages();

      if (!serverResponse) {
        setServerResponse(
`PENZI User Onfon
Welcome to our dating service with 6000 potential dating partners! 
To register SMS start#name#age#gender#county#town to 22141. 
E.g., start#John Doe#26#Male#Nakuru#Naivasha`
        );
        setNextStepGuide(
          "Start by sending: start#name#age#gender#county#town to 22141"
        );
      }
    };

    initialize();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchMessages = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/messages/");
      setMessages(res.data);
    } catch (err) {
      console.error("Failed to fetch messages:", err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!sender.trim() || !content.trim()) return;

    setLoading(true);

    // Show the message instantly in the UI
    const newMessage = {
      message_from: sender,
      message_to: "Server",
      content,
      direction: "OUTGOING",
      date_created: new Date().toISOString(),
    };
    setMessages((prev) => [newMessage, ...prev]);

    try {
      const res = await axios.post("http://localhost:8000/api/sms/", {
        message_from: sender,
        content,
      });

      // Show backend's response + guidance
      setServerResponse(res.data.response || "");
      setNextStepGuide(res.data.next_step_guide || "");

      // Refresh messages from backend
      await fetchMessages();

      // Clear input
      setContent("");
    } catch (err) {
      console.error("Error sending message:", err);
      setServerResponse("❌ Failed to send message.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "auto" }}>
      <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
        Send an SMS Command
      </h2>

      {/* Form */}
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Sender's phone number"
          value={sender}
          onChange={(e) => setSender(e.target.value)}
          style={{
            padding: "10px",
            width: "100%",
            marginBottom: "10px",
            border: "1px solid #ccc",
            borderRadius: "5px",
          }}
        />
        <input
          type="text"
          placeholder="Message content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          style={{
            padding: "10px",
            width: "100%",
            marginBottom: "10px",
            border: "1px solid #ccc",
            borderRadius: "5px",
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "10px 20px",
            background: "#d63384",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          {loading ? "Sending..." : "Send Message"}
        </button>
      </form>

      {/* Server response */}
      {serverResponse && (
        <div
          style={{
            background: "#f8f9fa",
            padding: "10px",
            borderRadius: "6px",
            border: "1px solid #ddd",
            marginBottom: "10px",
            whiteSpace: "pre-line",
          }}
        >
          <strong>Server Response:</strong> <br /> {serverResponse}
        </div>
      )}

      {/* Next step guide */}
      {nextStepGuide && (
        <div
          style={{
            background: "#fff3cd",
            padding: "10px",
            borderRadius: "6px",
            border: "1px solid #ffeeba",
            color: "#856404",
            marginBottom: "15px",
          }}
        >
          📌 <strong>Next Step:</strong> {nextStepGuide}
        </div>
      )}

      {/* Messages history */}
      <h3 style={{ marginBottom: "10px" }}>Message History</h3>
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "5px",
          padding: "10px",
          background: "#f8f9fa",
        }}
      >
        {messages.length === 0 ? (
          <p>No messages yet.</p>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              style={{
                marginBottom: "15px",
                padding: "10px",
                background:
                  msg.direction === "OUTGOING" ? "#d4edda" : "#cce5ff",
                borderRadius: "5px",
              }}
            >
              <div>
                <strong>{msg.message_from}</strong> ➡{" "}
                <strong>{msg.message_to}</strong>
              </div>
              <div>{msg.content}</div>
              {msg.next_step_guide && (
                <div
                  style={{
                    background: "#fff3cd",
                    border: "1px solid #ffeeba",
                    padding: "5px",
                    borderRadius: "3px",
                    marginTop: "5px",
                    fontSize: "0.9em",
                  }}
                >
                  <strong>Next Step:</strong> {msg.next_step_guide}
                </div>
              )}
              <small style={{ color: "#666" }}>
                {new Date(msg.date_created).toLocaleString()}
              </small>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
