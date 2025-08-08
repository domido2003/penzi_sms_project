import React, { useState, useEffect } from "react";
import axios from "axios";

function MessageForm() {
  const [messageFrom, setMessageFrom] = useState("");
  const [content, setContent] = useState("");
  const [messages, setMessages] = useState([]);
  const [responseMessage, setResponseMessage] = useState("");

  const fetchMessages = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/messages/");
      setMessages(response.data);
    } catch (error) {
      console.error("❌ Failed to fetch messages", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://localhost:8000/api/messages/", {
        message_from: messageFrom,
        content: content,
      });
      setResponseMessage(response.data.message);
      setMessageFrom("");
      setContent("");
      fetchMessages();
    } catch (error) {
      console.error("❌ Failed to send message", error);
      setResponseMessage("Failed to send message.");
    }
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  return (
    <div className="container mt-4">
      <div className="card p-4 shadow-sm">
        <h2 className="mb-3 text-primary">Send SMS Message</h2>
        <form onSubmit={handleSubmit} className="mb-4">
          <div className="mb-3">
            <label className="form-label">Sender Phone Number</label>
            <input
              type="text"
              value={messageFrom}
              onChange={(e) => setMessageFrom(e.target.value)}
              className="form-control"
              placeholder="e.g. 0712345678"
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Message Content</label>
            <input
              type="text"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="form-control"
              placeholder="e.g. start#john doe#23#male#nairobi#karen"
              required
            />
          </div>
          <button type="submit" className="btn btn-success">
            Send Message
          </button>
        </form>

        {responseMessage && (
          <div className="alert alert-info">{responseMessage}</div>
        )}
      </div>

      <div className="mt-5">
        <h4 className="mb-3 text-secondary">Message History</h4>
        <ul className="list-group">
          {messages.map((msg) => (
            <li key={msg.id} className="list-group-item">
              <strong>{msg.direction === "INCOMING" ? "From" : "To"}:</strong>{" "}
              {msg.message_from || msg.message_to}
              <br />
              <strong>Message:</strong> {msg.content}
              <br />
              <small className="text-muted">
                {new Date(msg.date_created).toLocaleString()}
              </small>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default MessageForm;
